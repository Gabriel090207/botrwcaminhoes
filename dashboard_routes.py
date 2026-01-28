from flask import jsonify
from datetime import date

def register_dashboard_routes(app, sessoes):

    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        hoje = date.today()

        conversas_hoje = 0
        em_andamento = 0
        transferidas = 0

        for sessao in sessoes.values():
            ultima = sessao.get("ultima_mensagem_cliente")

            if ultima and ultima.date() == hoje:
                conversas_hoje += 1

            if sessao.get("pausado_para_gabriel"):
                transferidas += 1
            else:
                em_andamento += 1

        return jsonify({
            "conversasHoje": conversas_hoje,
            "emAndamento": em_andamento,
            "transferidas": transferidas,
            "statusBot": "Ativo"
        })


    # 🔥 NOVO ENDPOINT DO GRÁFICO
    @app.route("/dashboard/conversas-hora", methods=["GET"])
    def conversas_por_hora():
        hoje = date.today()
        por_hora = {}

        for sessao in sessoes.values():
            ultima = sessao.get("ultima_mensagem_cliente")

            if ultima and ultima.date() == hoje:
                hora = ultima.strftime("%Hh")
                por_hora[hora] = por_hora.get(hora, 0) + 1

        # ordena por hora
        resultado = [
            {"hora": h, "conversas": por_hora[h]}
            for h in sorted(por_hora.keys())
        ]

        return jsonify(resultado)
