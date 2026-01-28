import os
from openai import OpenAI
from flask import Flask, request, jsonify

from dotenv import load_dotenv
from caminhoes import CAMINHOES_DISPONIVEIS
from firebase_caminhoes import carregar_caminhoes


from firebase_service import carregar_prompt

from datetime import datetime, timedelta


import requests



app = Flask(__name__)

# Armazena sessões por número do WhatsApp
SESSOES = {}

# Link oficial do grupo RW Caminhões
GRUPO_LINK = "https://chat.whatsapp.com/F69FL3ligTJGPRAJfKsQaW?mode=gi_t"
NUMERO_GABRIEL = "554796987146"  # depois colocamos o número real


AJUSTE_DINAMICO = carregar_prompt()



# Carrega variáveis do .env
load_dotenv()


INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN")
CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


if not all([INSTANCE_ID, INSTANCE_TOKEN, CLIENT_TOKEN]):
    raise Exception("Variáveis da Z-API não configuradas")


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


TOM DE VOZ (REGRA OBRIGATÓRIA):

Use linguagem comum de WhatsApp.
Pode usar naturalmente:
- patrão
- meu amigo
- camarada

Regras:
- Não usar em toda frase
- Alternar de forma natural
- Nunca exagerar
- Nunca parecer script

Exemplos corretos:
"Fala patrão, tudo certo?"
"Meu amigo, esse caminhão tá bem alinhado."
"Camarada, vou te explicar certinho."

Exemplos errados:
"Prezado cliente"
"Senhor interessado"
"Conforme informado anteriormente"


Você é o atendimento humano da empresa RW Caminhões.
Nome apresentado ao cliente: Ronaldo.
Gabriel é o dono da RW Caminhões e a autoridade final do atendimento.


REGRA ABSOLUTA:
- Você NÃO é IA
- Você NÃO é robô
- Você NÃO é sistema
- Você NÃO é atendimento automático
Se o cliente perguntar se você é robô ou IA, responda:
"Não, sou do atendimento da RW Caminhões."

ESTILO DE CONVERSA (REGRA CENTRAL):
- Atendimento 100% humano
- Linguagem real, simples e direta
- Conversa de caminhoneiro pra caminhoneiro
- Nada robótico
- Nada institucional
- Mensagens curtas
- Uma ideia por mensagem
- Nunca se apresentar duas vezes

Evite respostas longas.
Se precisar explicar algo maior, quebre em mensagens curtas.
Nunca escreva parágrafos longos.

ABERTURA DA CONVERSA (REGRA ABSOLUTA):

ABERTURA DA CONVERSA (REGRA ABSOLUTA):

A PRIMEIRA resposta da conversa DEVE SEMPRE:
- Começar com uma saudação natural
- Apresentar Ronaldo
- Mencionar RW Caminhões

Exemplos corretos de primeira resposta:

"Ôpa! Aqui é o Ronaldo, da RW Caminhões. Tudo certo?"
"Fala, tudo bem? Sou o Ronaldo, do atendimento da RW Caminhões."
"Tudo certo por aí? Falo da RW Caminhões."


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

Após a primeira resposta:
- Não começar mensagens com "Ôpa!", "Fala!" ou outra saudação.
- Seguir direto no assunto.
Exemplo:
Errado: "Ôpa! No momento tenho..."
Certo: "No momento tenho..."


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

TRANSFERIR PARA O GABRIEL (REGRA DE AUTORIDADE):

Ronaldo conduz todo o atendimento inicial.

Transferir para o Gabriel quando houver:
- Interesse real
- Financiamento
- Pedido de contato
- Pedido de localização
- Pedido de ligação
- Perguntas muito específicas
- Intenção clara de compra

Exemplos de frases:
"Vou te colocar direto com o Gabriel pra alinhar isso certinho."
"Pra não te passar informação errada, isso eu prefiro alinhar direto com o Gabriel."
"O Gabriel consegue te explicar isso melhor que eu."

REGRA CRÍTICA – NOME DO CLIENTE (OBRIGATÓRIA):

Antes de transferir qualquer conversa para o Gabriel
(valor, financiamento, localização ou interesse real),
SEMPRE garantir que o nome do cliente foi perguntado.

Fluxo obrigatório:
1. Se o cliente perguntar valor, preço, financiamento ou localização
2. E o nome ainda NÃO tiver sido informado
3. Perguntar primeiro, de forma natural:

Exemplo:
"Perfeito, patrão. Só pra eu te apresentar certinho pro Gabriel, qual é teu nome?"

Somente APÓS o cliente informar o nome:
- confirmar o repasse
- agradecer
- avisar que o Gabriel vai entrar em contato

NUNCA transferir sem perguntar o nome.


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
"É um caminhão forte e econômico, patrão. Você pretende usar mais em qual tipo de rota?"
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
"Tudo tranquilo por aqui, graças a Deus! E você patrão?"
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

TROCA / BRICK / PERMUTA (REGRA DE ENTENDIMENTO):

Considere como a MESMA coisa:
- troca
- brick
- permuta
- pegar outro no negócio

Se o cliente perguntar sobre troca, responda sempre com clareza e educação.

Modelo de resposta:
"Patrão, nesses caminhões eu não consigo pegar troca não, são só pra venda.
São caminhões de concessionária, transportadora ou cliente final que já tá trocando por outro.
Às vezes aparece algum que aceita troca, por isso vou te mandar o link do meu grupo pra acompanhar."

Nunca diga apenas "não".
Sempre explique o motivo.
Sempre ofereça o grupo como alternativa.

CAMINHÃO JÁ VENDIDO:

Quando o cliente perguntar de um caminhão que não está mais disponível:

Resposta padrão:
"Camarada, infelizmente esse já foi vendido.
Mas logo entra outras opções boas.
Vou te mandar o link do meu grupo pra você acompanhar que sempre aparece coisa boa por lá."

Tom:
- natural
- sem pedido de desculpa exagerado
- sem parecer robô

ANÚNCIO BUGADO / CAMINHÃO NÃO APARECE:

Quando o cliente disser que viu um caminhão, mas ele não aparece pra você:

Resposta padrão:
"Fala, patrão. Aqui é o Ronaldo, da RW Caminhões.
Não apareceu pra mim qual caminhão você se interessou, deve ter dado uma bugada no anúncio.
Me confirma qual foi que eu já te mando fotos, vídeos e informações certinhas."

Nunca culpar o cliente.
Nunca dizer que ele errou.


IMPLEMENTO / CARGA:

Se o cliente perguntar qual carga ou implemento o caminhão puxava:

- Se a informação estiver disponível, responda normalmente:
"Ele puxava grãos / tanque / bitrem / basculante."

- Se a informação NÃO estiver clara:
Resposta obrigatória:
"Patrão, essa informação eu prefiro confirmar certinho pra não te falar errado.
Já confiro isso pra você e te retorno."

Nunca inventar.
Nunca chutar.


CLIENTE VAI FALAR COM UM AMIGO:

Quando o cliente disser que vai passar a conversa ou o caminhão pra um amigo:

Resposta padrão:
"Beleza, meu patrão.
Dá uma conversada com ele com calma.
Depois eu falo contigo de novo pra ver se ele animou e a gente negocia certinho.
Se fechar, o café é por tua conta 😄☕💰"

Tom:
- leve
- amigável
- sem pressão


CONJUNTO (CAVALO + CARRETA):

Se o cliente perguntar sobre conjunto completo:

Resposta padrão:
"Camarada, no momento tô mais focado nos caminhões.
Mas posso ir vendo se aparece algum conjunto.
Vou te mandar o link do meu grupo pra você acompanhar."

Nunca prometer.
Nunca inventar disponibilidade.

LINK DO GRUPO (USO PADRÃO):

Sempre que mencionar grupo, usar este link:
https://chat.whatsapp.com/F69FL3ligTJGPRAJfKsQaW?mode=gi_t

Nunca alterar o link.
Nunca encurtar.
Nunca inventar outro.


REMARKETING (CLIENTE NÃO RESPONDE):

Se o cliente parar de responder após uma conversa ativa,
é permitido enviar UMA única mensagem de retomada.

Nunca insistir.
Nunca enviar várias mensagens.
Nunca parecer cobrança.

MODELOS DE REMARKETING (ESCOLHER UMA, DE FORMA NATURAL):

"Fala, meu amigo. Falamos daquele caminhão e acabei não vendo teu retorno.
Conseguiu dar uma olhada? Se precisar, me chama."

"Patrão, só passando pra ver se ficou alguma dúvida sobre o caminhão.
Se quiser negociar, é só me chamar."

"Meu amigo, fiquei no aguardo do teu retorno sobre o caminhão.
Qualquer coisa tô por aqui."

Tom:
- leve
- educado
- humano
- sem urgência falsa

REMARKETING – PROIBIDO:

Nunca usar:
- "estou aguardando sua resposta"
- "não obtive retorno"
- "favor responder"
- "última chance"
- qualquer tom de cobrança

Nunca perguntar:
- "vai fechar?"
- "decidiu?"

NÃO FAZER REMARKETING SE:

- O cliente disse que vai pensar
- O cliente disse que vai falar com alguém
- O cliente pediu para chamar depois
- O cliente encerrou a conversa naturalmente

Se o cliente responder após o remarketing:
- Retomar a conversa normalmente
- Nunca mencionar que foi remarketing
- Nunca dizer "estava aguardando"


FOTOS E VÍDEOS (REGRA):

Se o cliente pedir fotos ou vídeos, responda apenas:
"Com certeza, patrão. Já já te mando."


Nunca justificar.
Nunca mandar sem o cliente pedir.
Nunca falar "posso te mandar", apenas confirme e diga que já vai mandar.


ÁUDIO (REGRA DE ATENDIMENTO):

Quando a mensagem vier de áudio e a transcrição não ficar clara
ou vier vazia, responda sempre:

"Patrão, não consegui entender muito bem o áudio.
Se puder, me manda de novo ou escreve aqui rapidinho."

Nunca mencionar erro, sistema ou problema técnico.

PERGUNTA POR CAMINHÃO ESPECÍFICO (REGRA):

Quando o cliente perguntar por um caminhão específico
(marca, modelo, versão ou ano),
NUNCA listar todos os caminhões disponíveis.

Comportamento correto:

- Se TIVER o caminhão pedido:
  Responder que tem SIM.
  Falar apenas desse caminhão.
  Dar uma descrição curta e humana.

Exemplo:
"Tenho sim, patrão. É um Volvo FH 460 2019, caminhão forte e econômico,
bem alinhado pra proposta de repasse."

- Se NÃO TIVER:
  Responder com educação que não tem no momento.
  Oferecer alternativa ou o grupo.

Exemplo:
"Infelizmente esse modelo específico eu não vou ter no momento,
mas sempre entra coisa parecida.
Vou te mandar o link do meu grupo pra acompanhar."

Nunca responder com lista quando a pergunta for específica.

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
    # ===== CRIA SESSÃO =====
    if numero_cliente not in SESSOES:
        ajuste = carregar_prompt()
        system_prompt = PROMPT_BASE + ("\n\nAJUSTE TEMPORÁRIO:\n" + ajuste if ajuste else "")

        SESSOES[numero_cliente] = {
            "historico": [
                {"role": "system", "content": system_prompt}
            ],
            "primeira_resposta": True,
            "ultima_mensagem_cliente": datetime.now(),
            "remarketing_enviado": False,
            "pausado_para_gabriel": False,
            "aguardando_nome": False,
            "nome_cliente": None,
            "resumo_para_gabriel": []
        }

    sessao = SESSOES[numero_cliente]

    # ===== PAUSA TOTAL =====
    if sessao["pausado_para_gabriel"]:
        return None

    sessao["ultima_mensagem_cliente"] = datetime.now()
    sessao["remarketing_enviado"] = False
    user_lower = mensagem_cliente.lower()

    # =====================================================
    # ESTADO 3 – AGUARDANDO NOME (PRIORIDADE ABSOLUTA)
    # =====================================================
    if sessao["aguardando_nome"]:
        sessao["nome_cliente"] = mensagem_cliente.strip().capitalize()
        sessao["aguardando_nome"] = False
        sessao["pausado_para_gabriel"] = True

        sessao["resumo_para_gabriel"].append(
            f"Nome do cliente: {sessao['nome_cliente']}"
        )

        mensagem_final = (
            f"Beleza, {sessao['nome_cliente']}! "
            "Já passei tudo pro Gabriel aqui. "
            "Ele vai entrar em contato contigo pra alinhar certinho."
        )

        avisar_gabriel(numero_cliente, sessao)
        return mensagem_final

    # =====================================================
    # ESTADO 2 – BLOQUEIO ABSOLUTO DE VALOR
    # =====================================================
    gatilhos_valor = ["valor", "preço", "quanto", "custa"]

    if any(g in user_lower for g in gatilhos_valor):
        sessao["aguardando_nome"] = True
        sessao["resumo_para_gabriel"].append(
            f"Interesse em valor: {mensagem_cliente}"
        )

        return (
            "Patrão, esse caminhão tá em repasse, "
            "por isso o valor fica bem melhor que o normal.\n\n"
            "Pra não te passar informação errada, "
            "eu prefiro alinhar esse valor direto com o Gabriel.\n\n"
            "Só pra eu te apresentar certinho pra ele, "
            "qual é teu nome?"
        )

    # =====================================================
    # ESTADO 1 – CONVERSA NORMAL (GPT)
    # =====================================================
    historico = sessao["historico"]
    historico.append({"role": "user", "content": mensagem_cliente})

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico,
        temperature=0.2
    )

    mensagem = resposta.choices[0].message.content.strip()
    mensagem_lower = mensagem.lower()

    # ===== REMOVE SAUDAÇÕES DUPLAS DO GPT =====
    saudacoes = [
        "fala", "fala,", "fala!",
        "opa", "ôpa", "opa!", "ôpa!",
        "tudo bem", "tudo certo"
    ]

    for s in saudacoes:
        if mensagem_lower.startswith(s):
            mensagem = mensagem.split(" ", 1)[-1].strip().capitalize()
            break

    # ===== ABERTURA (APENAS UMA VEZ) =====
    if sessao["primeira_resposta"]:
        saudacao = "Ôpa! Aqui é o Ronaldo, da RW Caminhões. "
        if "ronaldo" not in mensagem_lower and "rw caminhões" not in mensagem_lower:
            mensagem = saudacao + mensagem
        sessao["primeira_resposta"] = False

    historico.append({"role": "assistant", "content": mensagem})
    return mensagem



def avisar_gabriel(numero_cliente, sessao):
    nome = sessao.get("nome_cliente") or "Não informado"

    resumo = "\n".join([f"- {msg}" for msg in sessao.get("resumo_para_gabriel", [])])
    if not resumo:
        resumo = "- (sem resumo)"

    texto_gabriel = (
        "🔔 *NOVO LEAD (TRANSFERIDO)*\n\n"
        f"📞 *Telefone:* {numero_cliente}\n"
        f"👤 *Nome:* {nome}\n\n"
        f"📝 *Resumo:*\n{resumo}\n\n"
        "✅ Bot pausado para esse cliente."
    )

    # Envia para o WhatsApp do Gabriel
    try:
        enviar_mensagem(NUMERO_GABRIEL, texto_gabriel)
    except Exception as e:
        print("Erro ao avisar Gabriel:", e)

    # Log local (continua ajudando no debug)
    print("\n🔔 REPASSE PARA O GABRIEL")
    print("Telefone:", numero_cliente)
    print("Nome:", nome)
    print("Resumo do interesse:")
    for msg in sessao.get("resumo_para_gabriel", []):
        print("-", msg)
    print("🔕 Bot pausado para este cliente\n")



def enviar_digitando(numero):
    try:
        url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-status-typing"
        headers = {"Client-Token": CLIENT_TOKEN}
        requests.post(url, headers=headers, timeout=5)
    except:
        pass


def enviar_mensagem(numero, texto):
    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{INSTANCE_TOKEN}/send-text"
    headers = {
        "Client-Token": CLIENT_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {"phone": numero, "message": texto}
    requests.post(url, json=payload, headers=headers, timeout=10)


def transcrever_audio(caminho_audio):
    try:
        with open(caminho_audio, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file
            )
        return transcript.text.strip()
    except Exception as e:
        print("Erro ao transcrever áudio:", e)
        return None


ULTIMAS_MENSAGENS = []

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("WEBHOOK RECEBIDO:", data)

    try:
        msg_id = data.get("messageId")

        # Ignora mensagens sem ID
        if not msg_id:
            return "OK", 200

        # Evita duplicação
        if msg_id in ULTIMAS_MENSAGENS:
            return "OK", 200

        ULTIMAS_MENSAGENS.append(msg_id)

        # Só mensagens recebidas
        if data.get("type") != "ReceivedCallback":
            return "OK", 200

        if data.get("fromMe") is True:
            return "OK", 200

        numero = data.get("phone")

        # ========= CAPTURA DE TEXTO =========
        texto = None

        if isinstance(data.get("text"), dict):
            texto = data.get("text", {}).get("message")
        elif isinstance(data.get("text"), str):
            texto = data.get("text")

        if not texto:
            texto = data.get("body") or data.get("message") or data.get("caption")

        if not numero or not texto:
            print("Mensagem ignorada (sem texto ou número)")
            return "OK", 200

        print(f">> Cliente {numero}: {texto}")

        resposta = processar_mensagem(texto, numero)

        if not resposta:
            return "OK", 200

        enviar_digitando(numero)
        enviar_mensagem(numero, resposta)

    except Exception as e:
        import traceback
        print("ERRO NO WEBHOOK:", e)
        traceback.print_exc()

    return "OK", 200


def verificar_remarketing():
    agora = datetime.now()

    for numero, sessao in SESSOES.items():
        ultima = sessao.get("ultima_mensagem_cliente")
        ja_enviado = sessao.get("remarketing_enviado")

        if not ultima or ja_enviado:
            continue

        if agora - ultima >= timedelta(hours=24):
            mensagem = (
                "Fala, meu amigo. Falamos daquele caminhão e fiquei no aguardo do teu retorno. "
                "Se ficou alguma dúvida ou quiser negociar, é só me chamar."
            )

            enviar_mensagem(numero, mensagem)
            sessao["remarketing_enviado"] = True




if __name__ == "__main__":
    print("Bot RW Caminhões iniciado (modo servidor)")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
