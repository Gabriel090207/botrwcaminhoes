import os
import re
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Importações dos seus arquivos locais
from firebase_caminhoes import carregar_caminhoes
from firebase_service import carregar_prompt
from dashboard_routes import register_dashboard_routes
from enviar_imagens import enviar_imagens_caminhao

# Carrega variáveis do .env
load_dotenv()

# Configurações Z-API e OpenAI
INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")
CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Armazena sessões por número do WhatsApp
SESSOES = {}

app = Flask(__name__)
CORS(app)
register_dashboard_routes(app, SESSOES)

NUMERO_GABRIEL = "5547991117146"

# --- SEU PROMPT ABSOLUTO INTEGRADO ---
PROMPT_BASE_SISTEMA = """
TOM DE VOZ (REGRA OBRIGATÓRIA):
Use linguagem comum de WhatsApp. Pode usar naturalmente: patrão, meu amigo, camarada.
Regras: Não usar em toda frase, alternar de forma natural, nunca exagerar, nunca parecer script.

Você é o atendimento humano da empresa RW Caminhões. Nome apresentado: Ronaldo.
Gabriel é o dono e a autoridade final.

REGRA ABSOLUTA: Você NÃO é IA, NÃO é robô. Se perguntarem, responda: "Não, sou do atendimento da RW Caminhões."
ESTILO: Mensagens curtas, uma ideia por mensagem, conversa de caminhoneiro pra caminhoneiro.

ABERTURA (REGRA ABSOLUTA): A PRIMEIRA resposta deve sempre saudar, apresentar Ronaldo e mencionar RW Caminhões.
NÃO liste caminhões automaticamente na primeira mensagem, a menos que perguntado.

POSICIONAMENTO: Caminhões são de REPASSE (sem maquiagem, preço melhor).
FINANCIAMENTO: Nunca garanta aprovação. Diga que a financeira (geralmente BV) analisa.
LOCALIZAÇÃO: NUNCA informe cidade ou pátio. Transfira para o Gabriel.

TRANSFERIR PARA O GABRIEL: Sempre pergunte o nome do cliente antes de transferir.
VALOR: Ignore centavos. Use apenas "310 mil" ou "1 milhão". Nunca use R$ ou formato bancário.

LINGUAGEM TÉCNICA: toco=4x2, truck=6x2, traçado=6x4, bitruck=8x2.
TROCA: Não aceita. Diga que são de repasse e ofereça o link do grupo: https://chat.whatsapp.com/F69FL3ligTJGPRAJfKsQaW?mode=gi_t
"""

# --- FUNÇÕES DE LÓGICA ---

def montar_contexto_estoque():
    """Busca os caminhões no Firebase e formata para o GPT."""
    caminhoes = carregar_caminhoes()
    blocos = []
    for c in caminhoes:
        if not c.get("ativo", True): continue
        bloco = f"- Marca: {c.get('marca')} | Modelo: {c.get('modelo')} | Ano: {c.get('ano')} | Tração: {c.get('tracao')} | Valor: {c.get('valor')} | Obs: {c.get('observacao', 'Repasse direto')}"
        blocos.append(bloco)
    return "\n".join(blocos) if blocos else "Nenhum caminhão disponível no momento."

def montar_prompt_final_dinamico():
    """Une seu prompt absoluto + estoque real + ajustes do painel."""
    estoque = montar_contexto_estoque()
    ajuste_dinamico = carregar_prompt()
    
    prompt = f"""
{PROMPT_BASE_SISTEMA}

CAMINHÕES DISPONÍVEIS (SISTEMA):
{estoque}

⚠️ AJUSTE TEMPORÁRIO (AVISO INTERNO):
{ajuste_dinamico if ajuste_dinamico else "Nenhum."}
"""
    return prompt

def detectar_caminhao_no_texto(texto, caminhoes):
    if not texto: return None
    t = texto.lower().replace("x", " ")
    for c in caminhoes:
        if not c.get("ativo", True): continue
        marca = (c.get("marca") or "").lower()
        modelo = (c.get("modelo") or "").lower()
        if (marca in t and any(p in t for p in modelo.split())) or \
           any(p in t for p in modelo.split() if p.isdigit() and len(p) >= 3):
            return c
    return None

def detectar_pedido_foto(texto: str) -> bool:
    palavras = ["foto", "fotos", "imagem", "imagens", "vídeo", "video", "videos", "vídeos"]
    return any(p in texto.lower() for p in palavras)

def limpar_resposta_whatsapp(texto: str) -> str:
    if not texto: return ""
    t = re.sub(r'([!?.,]){2,}', r'\1', texto)
    return t.strip()

def enviar_mensagem(numero, texto):
    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-text"
    headers = {"Client-Token": CLIENT_TOKEN, "Content-Type": "application/json"}
    payload = {"phone": numero, "message": texto}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10)
    except Exception as e:
        print("Erro Z-API:", e)

# --- ROTA WEBHOOK ---

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    try:
        if not data or data.get("fromMe"): return "OK", 200
        numero = data.get("phone")
        texto = (data.get("body") or data.get("text", {}).get("message") or "").strip()
        if not numero or not texto: return "OK", 200

        # Inicia sessão com seu prompt completo
        if numero not in SESSOES:
            SESSOES[numero] = {
                "caminhao_em_foco": None,
                "caminhoes_base": carregar_caminhoes(),
                "historico": [{"role": "system", "content": montar_prompt_final_dinamico()}],
                "pausado_para_gabriel": False,
                "aguardando_nome": False,
                "resumo_para_gabriel": []
            }
        
        sessao = SESSOES[numero]
        if sessao["pausado_para_gabriel"]: return "OK", 200
        sessao["resumo_para_gabriel"].append(f"Cliente: {texto}")

        # 1. PRIORIDADE: FOTOS (Bug Fix)
        if detectar_pedido_foto(texto):
            novo_foco = detectar_caminhao_no_texto(texto, sessao["caminhoes_base"])
            if novo_foco: sessao["caminhao_em_foco"] = novo_foco
            
            foco = sessao.get("caminhao_em_foco")
            if foco:
                enviar_mensagem(numero, "Com certeza, patrão. Já te mando.")
                enviar_imagens_caminhao(numero, foco.get("imagens", []), limite=15)
                return "OK", 200
            else:
                enviar_mensagem(numero, "Com certeza! Só me confirma qual caminhão você quer ver as fotos?")
                return "OK", 200

        # 2. CAPTURA DE NOME
        if sessao["aguardando_nome"]:
            nome = texto.split()[0].capitalize()
            enviar_mensagem(numero, f"Valeu, {nome}! 👍 O Gabriel já vai entrar em contato contigo.")
            sessao["pausado_para_gabriel"] = True
            return "OK", 200

        # 3. ATUALIZA FOCO
        achado = detectar_caminhao_no_texto(texto, sessao["caminhoes_base"])
        if achado: sessao["caminhao_em_foco"] = achado

        # 4. RESPOSTA RONALDO (GPT)
        sessao["historico"].append({"role": "user", "content": texto})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=sessao["historico"],
            temperature=0.3
        )
        resposta_gpt = limpar_resposta_whatsapp(response.choices[0].message.content)
        sessao["historico"].append({"role": "assistant", "content": resposta_gpt})

        if "qual é teu nome" in resposta_gpt.lower() or "qual seu nome" in resposta_gpt.lower():
            sessao["aguardando_nome"] = True

        # Envia em partes para parecer humano
        for msg in re.split(r'(?<=[.!?])\s+', resposta_gpt):
            if msg.strip():
                enviar_mensagem(numero, msg.strip())
                time.sleep(1.2)

    except Exception as e:
        print(f"Erro: {e}")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))