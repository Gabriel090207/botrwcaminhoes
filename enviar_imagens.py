import time
import requests

def enviar_imagens_caminhao(numero, imagens, limite=20):
    """
    Envia imagens do caminhão UMA POR VEZ via Z-API,
    garantindo que o WhatsApp renderize corretamente.
    """

    if not imagens:
        return

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-image"

    headers = {
        "Client-Token": CLIENT_TOKEN,
        "Content-Type": "application/json"
    }

    enviados = 0

    for img_url in imagens:
        if enviados >= limite:
            break

        # Segurança: só envia se for URL válida
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

            # ⏱️ Delay OBRIGATÓRIO (evita agrupamento como arquivo)
            time.sleep(1.5)

        except Exception as e:
            print("Erro ao enviar imagem:", e)
