import os
import requests

INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")
CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


def enviar_imagens_caminhao(numero, imagens, limite=3):
    """
    Envia imagens do caminhão via Z-API.
    Envia no máximo 'limite' imagens.
    """

    if not imagens:
        return False

    imagens = imagens[:limite]

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-image"
    headers = {
        "Client-Token": CLIENT_TOKEN,
        "Content-Type": "application/json"
    }

    for img_url in imagens:
        payload = {
            "phone": numero,
            "image": img_url
        }

        try:
            requests.post(url, json=payload, headers=headers, timeout=10)
        except Exception as e:
            print("Erro ao enviar imagem:", e)

    return True
