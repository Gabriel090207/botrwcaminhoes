from datetime import date
from firebase_admin import firestore

db = firestore.client()


def registrar_conversa():
    hoje = date.today().isoformat()
    ref = db.collection("dashboard_conversas").document(hoje)

    doc = ref.get()

    # cria estrutura base
    horas_base = {f"{h:02d}": 0 for h in range(24)}

    if not doc.exists:
        ref.set({
            "data": hoje,
            "total": 1,
            "porHora": horas_base,
            "atualizadoEm": firestore.SERVER_TIMESTAMP
        })
    else:
        dados = doc.to_dict()
        ref.update({
            "total": dados.get("total", 0) + 1,
            "atualizadoEm": firestore.SERVER_TIMESTAMP
        })
