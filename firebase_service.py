from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate("firebase-key.json")
initialize_app(cred)

db = firestore.client()

def carregar_prompt():
    doc = db.collection("bot_config").document("config").get()

    if not doc.exists:
        return None

    data = doc.to_dict()

    if data.get("ativo") is not True:
        return None

    return data.get("promptBase")
