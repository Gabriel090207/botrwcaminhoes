import requests
import os


def enviar_imagem_whatsapp(numero, url_imagem):

    instance = os.getenv("ZAPI_INSTANCE_ID")
    token = os.getenv("ZAPI_INSTANCE_TOKEN")

    url = f"https://api.z-api.io/instances/{instance}/token/{token}/send-image"

    payload = {
        "phone": numero,
        "image": url_imagem
    }

    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Erro enviando imagem:", e)
