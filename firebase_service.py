import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase usando arquivo JSON via variável de ambiente
if not firebase_admin._apps:
    firebase_key_path = os.getenv("FIREBASE_KEY_JSON")

    if not firebase_key_path:
        raise Exception("FIREBASE_KEY_JSON não configurado no ambiente")

    if not os.path.exists(firebase_key_path):
        raise Exception(f"Arquivo Firebase não encontrado: {firebase_key_path}")

    with open(firebase_key_path, "r", encoding="utf-8") as f:
        cred_dict = json.load(f)

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

