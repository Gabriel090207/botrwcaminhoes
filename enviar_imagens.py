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
    Adicionado suporte a cabeçalho data:image para evitar rejeição da API.
    """
    if not imagens:
        print("DEBUG: Nenhuma imagem recebida para enviar.")
        return False

    # Filtra links vazios e aplica o limite
    imagens_validas = [img for img in imagens if img and img.strip()][:limite]
    
    if not imagens_validas:
        return False

    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-image"
    headers = {
        "Client-Token": CLIENT_TOKEN,
        "Content-Type": "application/json"
    }

    print(f"DEBUG: Iniciando envio de {len(imagens_validas)} imagens para {numero}")

    for img_url in imagens_validas:
        try:
            # Baixa a imagem
            r = requests.get(img_url, timeout=15)
            if r.status_code != 200:
                print(f"DEBUG: Erro ao baixar imagem ({r.status_code}): {img_url}")
                continue

            # Converte para base64
            img_base64 = base64.b64encode(r.content).decode("utf-8")
            
            # A Z-API recomenda o formato completo do data URI
            payload = {
                "phone": numero,
                "image": f"data:image/jpeg;base64,{img_base64}"
            }

            response = requests.post(url, json=payload, headers=headers, timeout=20)
            
            if response.status_code not in [200, 201]:
                print(f"DEBUG: Z-API retornou erro {response.status_code}: {response.text}")
            else:
                print(f"DEBUG: Imagem enviada com sucesso: {img_url}")

            time.sleep(1.5)  # Delay para não banir o número e processar na fila

        except Exception as e:
            print(f"DEBUG: Exceção ao enviar imagem: {e}")

    return True