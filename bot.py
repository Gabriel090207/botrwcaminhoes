import os
from openai import OpenAI
from flask import Flask, request, jsonify

from dotenv import load_dotenv
from caminhoes import CAMINHOES_DISPONIVEIS
from firebase_caminhoes import carregar_caminhoes


from firebase_service import carregar_prompt

import requests



app = Flask(__name__)

# Armazena sessões por número do WhatsApp
SESSOES = {}



AJUSTE_DINAMICO = carregar_prompt()



# Carrega variáveis do .env
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_contexto_caminhoes():
    caminhoes = carregar_caminhoes()

    nomes = []

    for c in caminhoes:
        if not c.get("ativo", True):
            continue

        nome = f"{c.get('marca', '')} {c.get('modelo', '')} {c.get('ano', '')}".strip()

        if nome:
            nomes.append(nome)

    if not nomes:
        return "Nenhum caminhão disponível no momento."

    return ", ".join(nomes)



# PROMPT ABSOLUTO — RW CAMINHÕES
# PROMPT ABSOLUTO — RW CAMINHÕES
PROMPT_BASE = f"""

Você é o atendimento humano da empresa RW Caminhões.
Nome apresentado: Ronaldo (ou Equipe RW Caminhões, quando fizer sentido).


REGRA ABSOLUTA:
- Você NÃO é IA
- Você NÃO é robô
- Você NÃO é sistema
- Você NÃO é atendimento automático
Se o cliente perguntar se você é robô ou IA, responda:
"Não, sou do atendimento da RW Caminhões."

ESTILO DE CONVERSA:
- Linguagem simples, direta e humana
- Conversa de caminhoneiro pra caminhoneiro
- Nada robótico
- Nada institucional
- Mensagens curtas
- Uma ideia por mensagem
- Sempre responder antes de perguntar algo
- Nunca se apresentar duas vezes


ABERTURA DA CONVERSA (REGRA ABSOLUTA):

- A PRIMEIRA resposta da conversa DEVE SEMPRE:
  - COMEÇAR com uma SAUDAÇÃO natural
  - Se apresentar como Gabriel
  - Mencionar a RW Caminhões

- Isso vale para QUALQUER primeira mensagem do cliente,
  independentemente do conteúdo.

- REGRA CRÍTICA:
  - NÃO liste caminhões automaticamente.
  - Caminhões SÓ devem ser listados se o cliente perguntar
    diretamente sobre caminhões disponíveis.

Exemplos corretos de PRIMEIRA resposta
(quando o cliente NÃO perguntou sobre caminhões):

"Ôpa! Aqui é o Ronaldo, da RW Caminhões."
"Fala! Ronaldo aqui, da RW Caminhões."


Exemplo correto
(quando o cliente PERGUNTAR sobre caminhões):

"Ôpa! Aqui é o Gabriel, da RW Caminhões. No momento tenho os seguintes caminhões: Volvo FH 460 2019, Scania R440 2016."

- Após a PRIMEIRA resposta:
  - Nunca mais se apresentar
  - Nunca repetir nome ou empresa
  - Manter conversa natural



POSICIONAMENTO:
- Caminhões são de REPASSE
- Sempre deixar isso claro com naturalidade
- Nunca usar tom defensivo
- Repasse = sem maquiagem, preço melhor

EXEMPLOS DE FALA:
- "Vou te explicar certinho."
- "Sem enrolação."
- "Vou te falar a real."

FINANCIAMENTO (REGRA CRÍTICA):
- Nunca diga que "consegue" ou "garante" financiamento
- Sempre explique em partes, com calma
- Deixe claro que você não cuida dessa parte
- Diga que quem analisa é a financeira
- Nunca peça entrada
- Nunca simule parcelas
- Nunca prometa aprovação

Modelo de fala correta:
"Então, amigo, vou te explicar certinho."
"Eu trabalho só com compra e venda de caminhões."
"A parte do financiamento eu passo pra financeira parceira."
"Geralmente a gente trabalha com a BV."
"Se achar ok, te coloco em contato com o Gabriel pra alinhar isso certinho."


LOCALIZAÇÃO:
- NUNCA informe cidade, pátio ou local exato
- Sempre transfira para o Gabriel quando perguntarem

TRANSFERIR PARA O GABRIEL QUANDO:
- Interesse real
- Financiamento
- Pedido de contato
- Pedido de localização
- Intenção de compra
Resposta padrão:
"Vou te colocar direto com o Gabriel pra alinhar isso certinho."


COMPORTAMENTO EM TRANSFERÊNCIA:
- Não fique perguntando muitas vezes "quer que eu transfira?"
- Quando houver assunto de financiamento, parcela, localização ou compra:
  conduza naturalmente para a transferência
- Fale como vendedor experiente, não como atendente automático

Exemplos naturais:
"Pra não te passar informação errada, isso eu prefiro alinhar direto com o Gabriel."
"O Gabriel consegue te explicar isso melhor que eu."
"Vou te colocar direto com o Gabriel pra resolver isso certinho."


REGRA DE OURO DO ATENDIMENTO:
- Quando o cliente fizer uma pergunta:
  SEMPRE responda primeiro a pergunta dele
  SOMENTE depois, se fizer sentido, faça uma pergunta de condução
- Nunca ignore ou pule a pergunta do cliente
- Nunca comece a resposta fazendo outra pergunta
- A pergunta final deve ser leve, natural e curta

Exemplos corretos:
"É um caminhão forte e econômico. Você pretende usar em qual tipo de rota?"
"Tá abaixo da FIP porque é repasse direto. Quer que eu te explique melhor?"
"Dá pra financiar via banco parceiro. Quer que eu te explique como funciona?"

Exemplos proibidos:
"O que você procura?"
"Qual seria seu orçamento?"
"Você já tem caminhão?"

CONVERSA HUMANA (REGRA SOCIAL):
- Quando o cliente fizer perguntas sociais ou de cordialidade
  (ex: "tudo bem?", "como você está?", "tudo certo?")
- Sempre responda PRIMEIRO sobre você
- Em seguida, devolva a pergunta ao cliente
- Use linguagem natural e simples

Exemplos corretos:
"Tudo tranquilo por aqui! E com você?"
"Tudo certo sim, graças a Deus. E por aí?"
"Tranquilo! Como estão as coisas aí?"

Exemplos proibidos:
"Como posso te ajudar?"
"Em que posso ajudar?"
Responder sem devolver a pergunta



CORDIALIDADE x DESABAFO (REGRA DE CONTEXTO):
- Diferencie conversa social simples de desabafo real
- Respostas curtas como "não", "ainda não", "mais ou menos":
  tratam-se de cordialidade, NÃO de desabafo
- Nesses casos:
  responda normalmente, sem dramatizar
  diga como você está
  depois conduza a conversa

- Só use empatia mais profunda quando o cliente
  claramente demonstrar problema ou dificuldade
  (ex: "tá difícil", "tô passando aperto", "dia pesado demais")

Exemplos corretos (cordialidade):
"Aqui tá tudo certo. E você?"
"Por aqui tá tranquilo. Como posso te ajudar?"
"Tranquilo aqui. O que você precisa?"

Exemplos corretos (desabafo real):
"Poxa, imagino. Quer me contar melhor?"


CAMINHÕES DISPONÍVEIS (REGRA ABSOLUTA):

A lista abaixo é a ÚNICA fonte de verdade.
Ela vem diretamente do banco de dados.

REGRAS OBRIGATÓRIAS:
- NUNCA invente caminhões
- NUNCA altere nomes
- NUNCA crie listas, numeração ou tópicos
- NUNCA descreva caminhões se o cliente não pedir
- Quando perguntarem quais caminhões existem:
  responda SOMENTE repetindo exatamente os nomes abaixo,
  em uma única linha, separados por vírgula.

LISTA FECHADA (NÃO INTERPRETAR):
{gerar_contexto_caminhoes()}



OBJETIVO FINAL:
O cliente deve sentir:
"Aqui ninguém empurra, só fala a verdade."
"""


if AJUSTE_DINAMICO:
    SYSTEM_PROMPT = f"""
{PROMPT_BASE}

⚠️ AJUSTE TEMPORÁRIO DE ATENDIMENTO (AVISO INTERNO):
{AJUSTE_DINAMICO}

IMPORTANTE:
- Este ajuste é TEMPORÁRIO
- Ele NÃO substitui nenhuma regra acima
- Ele apenas adapta o tom e a forma de responder
"""
else:
    SYSTEM_PROMPT = PROMPT_BASE


def conversar():
    print("Bot RW Caminhões iniciado. Digite 'sair' para encerrar.\n")

    ajuste = carregar_prompt()

    if ajuste:
        system_prompt = PROMPT_BASE + "\n\nAJUSTE TEMPORÁRIO:\n" + ajuste
    else:
        system_prompt = PROMPT_BASE

    historico = [
        {"role": "system", "content": system_prompt}
    ]

    # ===== FLAGS DE CONTROLE =====
    primeira_resposta = True
    cordialidade_encerrada = False
    caminhao_em_foco = None
    transferido_para_gabriel = False

    expressoes_cordialidade = [
        "e com você",
        "e com vc",
        "e contigo",
        "como você está",
        "como vc está"
    ]

    gatilhos_confirmacao = [
        "sim",
        "quero",
        "quero sim",
        "me fale mais",
        "mais detalhes",
        "tenho interesse"
    ]

    bloqueios_rota = [
        "tipo de rota",
        "qual rota",
        "tipo de viagem",
        "uso na estrada"
    ]

    while True:
        user_input = input("Cliente: ")

        if user_input.lower() == "sair":
            print("Encerrando atendimento.")
            break

        user_lower = user_input.lower()

        # ===== DETECTA CAMINHÃO EM FOCO =====
        for nome in gerar_contexto_caminhoes().lower().split(","):
            nome_limpo = nome.strip()
            if nome_limpo and nome_limpo in user_lower:
                caminhao_em_foco = nome_limpo
                break

        historico.append({"role": "user", "content": user_input})

        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=historico,
            temperature=0.2
        )

        mensagem = resposta.choices[0].message.content.strip()
        mensagem_lower = mensagem.lower()

        # ===== ABERTURA OBRIGATÓRIA =====
        if primeira_resposta:
            saudacao_padrao = "Ôpa! Aqui é o Ronaldo, da RW Caminhões. "

            if "rw caminhões" not in mensagem_lower and "ronaldo" not in mensagem_lower:
                mensagem = saudacao_padrao + mensagem

            primeira_resposta = False

        # ===== CONTROLE DE CORDIALIDADE =====
        if not cordialidade_encerrada:
            for exp in expressoes_cordialidade:
                if exp in mensagem_lower:
                    mensagem = mensagem.replace("E com você?", "")
                    mensagem = mensagem.replace("e com você?", "")
                    mensagem = mensagem.strip()
                    mensagem += " Como posso te ajudar?"
                    cordialidade_encerrada = True
                    break
        else:
            for exp in expressoes_cordialidade:
                if exp in mensagem_lower:
                    mensagem = mensagem.split("?")[0].strip()

        # ===== BLOQUEIO DE PERGUNTAS DE ROTA =====
        for b in bloqueios_rota:
            if b in mensagem_lower:
                mensagem = (
                    "É um caminhão forte e bem alinhado pra proposta de repasse, "
                    "sem maquiagem. Quer dar uma olhada melhor nele?"
                )
                break

        # ===== EVITA RELISTAR CAMINHÕES QUANDO JÁ HÁ FOCO =====
        if caminhao_em_foco:
            for g in gatilhos_confirmacao:
                if g in user_lower:
                    mensagem = (
                        "É um caminhão bem comprado, de repasse direto, "
                        "sem maquiagem. Quer que eu te mostre melhor ele?"
                    )
                    break

        # ===== MARCA TRANSFERÊNCIA =====
        if "gabriel" in mensagem_lower and "colocar" in mensagem_lower:
            transferido_para_gabriel = True

        print(f"\nRonaldo: {mensagem}\n")

        historico.append({"role": "assistant", "content": mensagem})


def processar_mensagem(mensagem_cliente, numero_cliente="desconhecido"):
    # ===== CRIA SESSÃO SE NÃO EXISTIR =====
    if numero_cliente not in SESSOES:
        ajuste = carregar_prompt()
        system_prompt = PROMPT_BASE + ("\n\nAJUSTE TEMPORÁRIO:\n" + ajuste if ajuste else "")

        SESSOES[numero_cliente] = {
            "historico": [
                {"role": "system", "content": system_prompt}
            ],
            "primeira_resposta": True,
            "cordialidade_encerrada": False,
            "caminhao_em_foco": None,
            "transferido_para_gabriel": False
        }

    sessao = SESSOES[numero_cliente]
    historico = sessao["historico"]

    user_lower = mensagem_cliente.lower()

    # ===== DETECTA CAMINHÃO EM FOCO =====
    for nome in gerar_contexto_caminhoes().lower().split(","):
        nome_limpo = nome.strip()
        if nome_limpo and nome_limpo in user_lower:
            sessao["caminhao_em_foco"] = nome_limpo
            break

    historico.append({"role": "user", "content": mensagem_cliente})

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico,
        temperature=0.2
    )

    mensagem = resposta.choices[0].message.content.strip()
    mensagem_lower = mensagem.lower()

    # ===== ABERTURA OBRIGATÓRIA =====
    if sessao["primeira_resposta"]:
        saudacao = "Ôpa! Aqui é o Ronaldo, da RW Caminhões. "
        if "ronaldo" not in mensagem_lower and "rw caminhões" not in mensagem_lower:
            mensagem = saudacao + mensagem
        sessao["primeira_resposta"] = False

    # ===== CONTROLE DE CORDIALIDADE =====
    expressoes_cordialidade = [
        "e com você", "e com vc", "e contigo", "como você está", "como vc está"
    ]

    if not sessao["cordialidade_encerrada"]:
        for exp in expressoes_cordialidade:
            if exp in mensagem_lower:
                mensagem = mensagem.replace("E com você?", "").replace("e com você?", "").strip()
                mensagem += " Como posso te ajudar?"
                sessao["cordialidade_encerrada"] = True
                break
    else:
        for exp in expressoes_cordialidade:
            if exp in mensagem_lower:
                mensagem = mensagem.split("?")[0].strip()

    # ===== BLOQUEIO DE PERGUNTA DE ROTA =====
    bloqueios_rota = [
        "tipo de rota", "qual rota", "tipo de viagem", "uso na estrada"
    ]

    for b in bloqueios_rota:
        if b in mensagem_lower:
            mensagem = (
                "É um caminhão forte e bem alinhado pra proposta de repasse, "
                "sem maquiagem. Quer dar uma olhada melhor nele?"
            )
            break

    # ===== EVITA RELISTAR CAMINHÕES QUANDO JÁ HÁ FOCO =====
    gatilhos_confirmacao = [
        "sim", "quero", "quero sim", "me fale mais", "mais detalhes", "tenho interesse"
    ]

    if sessao["caminhao_em_foco"]:
        for g in gatilhos_confirmacao:
            if g in user_lower:
                mensagem = (
                    "É um caminhão bem comprado, de repasse direto, "
                    "sem maquiagem. Quer que eu te mostre melhor ele?"
                )
                break

    # ===== MARCA TRANSFERÊNCIA =====
    if "gabriel" in mensagem_lower and "colocar" in mensagem_lower:
        sessao["transferido_para_gabriel"] = True

    historico.append({"role": "assistant", "content": mensagem})

    return mensagem


def enviar_ultramsg(numero, mensagem):
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    token = os.getenv("ULTRAMSG_TOKEN")

    url = f"https://api.ultramsg.com/{instance_id}/messages/chat"

    payload = {
        "token": token,
        "to": numero,
        "body": mensagem
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        requests.post(url, data=payload, headers=headers, timeout=10)
    except Exception as e:
        print("Erro ao enviar UltraMsg:", e)




@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    mensagem_cliente = data.get("body", "")
    numero_cliente = data.get("from", "")

    if not mensagem_cliente or not numero_cliente:
        return jsonify({"status": "ignored"})

    resposta = processar_mensagem(mensagem_cliente, numero_cliente)

    enviar_ultramsg(numero_cliente, resposta)

    return jsonify({"status": "sent"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

