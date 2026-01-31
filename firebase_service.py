import os
import json
import firebase_admin
from firebase_admin import credentials, firestore


# =========================
# 🔥 INICIALIZA FIREBASE
# =========================
if not firebase_admin._apps:

    firebase_json = os.getenv("FIREBASE_KEY_JSON")

    # ===== CASO 1 — ENV (PRODUÇÃO / CLOUD)
    if firebase_json:
        try:
            cred_dict = json.loads(firebase_json)
            cred = credentials.Certificate(cred_dict)
            print("🔥 Firebase inicializado via ENV")
        except Exception:
            raise Exception("FIREBASE_KEY_JSON inválido")

    # ===== CASO 2 — ARQUIVO LOCAL (DEV / TERMINAL)
    else:
        print("🔥 Firebase inicializado via firebase-key.json local")

        if not os.path.exists("firebase-key.json"):
            raise Exception(
                "firebase-key.json não encontrado na raiz do projeto"
            )

        cred = credentials.Certificate("firebase-key.json")

    firebase_admin.initialize_app(cred)


# =========================
# 🔥 CLIENT FIRESTORE
# =========================
db = firestore.client()


# =========================
# 🔥 CARREGAR PROMPT DO FIRESTORE
# =========================
def carregar_prompt():

    try:
        doc = db.collection("bot_config").document("config").get()

        if not doc.exists:
            return None

        data = doc.to_dict()

        if data.get("ativo") is not True:
            return None

        return data.get("promptBase")

    except Exception as e:
        print("Erro ao carregar prompt:", e)
        return None
