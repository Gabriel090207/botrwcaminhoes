import os
import time
import base64
import requests

INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")
CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


def enviar_imagens_caminhao(numero, imagens, limite=3):
    """
    Envia imagens do caminhão via Z-API usando BASE64
    (forma mais confiável para WhatsApp).
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
        try:
            # baixa a imagem
            r = requests.get(img_url, timeout=15)
            if r.status_code != 200:
                print("Erro ao baixar imagem:", img_url)
                continue

            # converte para base64
            img_base64 = base64.b64encode(r.content).decode("utf-8")

            payload = {
                "phone": numero,
                "image": img_base64
            }

            requests.post(url, json=payload, headers=headers, timeout=10)

            time.sleep(1.5)  # evita agrupamento

        except Exception as e:
            print("Erro ao enviar imagem:", e)

    return True
