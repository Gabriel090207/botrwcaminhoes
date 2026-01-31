import os
import time
import base64
import requests

INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")
CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

def enviar_imagens_caminhao(numero, imagens, limite=3):
    """
    Envia imagens do caminhão via Z-API usando BASE64.
    Corrige falhas silenciosas e valida envio real.
    """

    if not imagens:
        print("DEBUG: Nenhuma imagem recebida.")
        return False

    imagens_validas = [img for img in imagens if img and img.strip()][:limite]

    if not imagens_validas:
        print("DEBUG: Lista vazia após filtro.")
        return False

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-image"
    headers = {
        "Client-Token": CLIENT_TOKEN,
        "Content-Type": "application/json"
    }

    print(f"DEBUG: Enviando {len(imagens_validas)} imagens para {numero}")

    enviadas = 0

    for img_url in imagens_validas:
        try:
            print("DEBUG: Baixando:", img_url)

            r = requests.get(img_url, timeout=20)

            if r.status_code != 200:
                print(f"DEBUG: Falha download {r.status_code}")
                continue

            content_type = r.headers.get("Content-Type", "image/jpeg")

            img_base64 = base64.b64encode(r.content).decode("utf-8")

            payload = {
                "phone": numero,
                "image": f"data:{content_type};base64,{img_base64}"
            }

            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=20
            )

            if response.status_code in [200, 201]:
                enviadas += 1
                print("DEBUG: Imagem enviada OK")
            else:
                print("DEBUG: Erro ZAPI:", response.text)

            time.sleep(2)

        except Exception as e:
            print("DEBUG: Exceção envio:", e)

    print(f"DEBUG: Total enviadas: {enviadas}")

    return enviadas > 0
