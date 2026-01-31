import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def enviar_imagens_caminhao(numero, imagens, limite=20):
    """
    Envia imagens do caminhão UMA POR VEZ via Z-API,
    garantindo que o WhatsApp renderize corretamente.
    Lê as credenciais diretamente do .env:
    - ZAPI_INSTANCE_ID
    - ZAPI_INSTANCE_TOKEN
    - ZAPI_CLIENT_TOKEN
    """

    instance_id = os.getenv("ZAPI_INSTANCE_ID")
    instance_token = os.getenv("ZAPI_INSTANCE_TOKEN")
    client_token = os.getenv("ZAPI_CLIENT_TOKEN")

    if not all([instance_id, instance_token, client_token]):
        print("Erro: variáveis Z-API não configuradas no .env")
        return

    if not imagens:
        return

    url = f"https://api.z-api.io/instances/{instance_id}/token/{instance_token}/send-image"

    headers = {
        "Client-Token": client_token,
        "Content-Type": "application/json"
    }

    enviados = 0

    for img_url in imagens:
        if enviados >= limite:
            break

        if not isinstance(img_url, str):
            continue

        if not img_url.startswith("http"):
            continue

        payload = {
            "phone": numero,
            "image": img_url
        }

        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code != 200:
                print("Erro ao enviar imagem:", response.text)

            enviados += 1
            time.sleep(1.5)

        except Exception as e:
            print("Erro ao enviar imagem:", e)
