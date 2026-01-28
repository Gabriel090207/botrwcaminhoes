import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase usando JSON direto da variável de ambiente
if not firebase_admin._apps:
    firebase_json = os.getenv("FIREBASE_KEY_JSON")

    if not firebase_json:
        raise Exception("FIREBASE_KEY_JSON não configurado no ambiente")

    try:
        cred_dict = json.loads(firebase_json)
    except Exception:
        raise Exception("FIREBASE_KEY_JSON não é um JSON válido")

    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

db = firestore.client()


def carregar_prompt():
    doc = db.collection("bot_config").document("config").get()

    if not doc.exists:
        return None

    data = doc.to_dict()

    if data.get("ativo") is not True:
        return None

    return data.get("promptBase")
