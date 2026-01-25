from firebase_service import db

def carregar_caminhoes():
    docs = db.collection("caminhoes").stream()

    caminhoes = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        caminhoes.append(data)

    return caminhoes
