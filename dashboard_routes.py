from flask import jsonify
from datetime import datetime, date
from firebase_admin import firestore

db = firestore.client()


def _estrutura_horas():
    return {f"{h:02d}": 0 for h in range(24)}


def _garantir_documento_dia():
    hoje = date.today().isoformat()
    ref = db.collection("dashboard_conversas").document(hoje)
    doc = ref.get()

    if not doc.exists:
        ref.set({
            "data": hoje,
            "total": 0,
            "porHora": _estrutura_horas(),
            "atualizadoEm": firestore.SERVER_TIMESTAMP
        })

    return ref


def registrar_conversa_dashboard():
    agora = datetime.now()
    hora = agora.strftime("%H")

    ref = _garantir_documento_dia()
    doc = ref.get().to_dict()

    por_hora = doc.get("porHora", _estrutura_horas())
    por_hora[hora] = por_hora.get(hora, 0) + 1

    ref.update({
        "total": doc.get("total", 0) + 1,
        "porHora": por_hora,
        "atualizadoEm": firestore.SERVER_TIMESTAMP
    })


def register_dashboard_routes(app, sessoes):

    # ===============================
    # DASHBOARD - CARDS
    # ===============================
    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        hoje = date.today().isoformat()
        ref = db.collection("dashboard_conversas").document(hoje)
        doc = ref.get()

        if not doc.exists:
            dados = {
                "total": 0
            }
        else:
            dados = doc.to_dict()

        return jsonify({
            "conversasHoje": dados.get("total", 0),
            "emAndamento": len([
                s for s in sessoes.values()
                if not s.get("pausado_para_gabriel")
            ]),
            "transferidas": len([
                s for s in sessoes.values()
                if s.get("pausado_para_gabriel")
            ]),
            "statusBot": "Ativo"
        })


    # ===============================
    # DASHBOARD - GRÁFICO POR HORA
    # ===============================
    @app.route("/dashboard/conversas-hora", methods=["GET"])
    def conversas_por_hora():
        hoje = date.today().isoformat()
        ref = db.collection("dashboard_conversas").document(hoje)
        doc = ref.get()

        horas = _estrutura_horas()

        if doc.exists:
            horas.update(doc.to_dict().get("porHora", {}))

        resultado = [
            {"hora": h, "conversas": horas[h]}
            for h in sorted(horas.keys())
        ]

        return jsonify(resultado)
