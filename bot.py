import os
from openai import OpenAI
from flask import Flask, request, jsonify

from dotenv import load_dotenv
from caminhoes import CAMINHOES_DISPONIVEIS
from firebase_caminhoes import carregar_caminhoes


from firebase_service import carregar_prompt

from datetime import datetime, timedelta


import requests

from dashboard_routes import register_dashboard_routes

from flask_cors import CORS

import time

from enviar_imagens import enviar_imagens_caminhao




# Armazena sessões por número do WhatsApp
SESSOES = {}

app = Flask(__name__)
CORS(app)
register_dashboard_routes(app, SESSOES)



# Link oficial do grupo RW Caminhões
GRUPO_LINK = "https://chat.whatsapp.com/F69FL3ligTJGPRAJfKsQaW?mode=gi_t"
NUMERO_GABRIEL = "5547991117146"  # depois colocamos o número real


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



def filtrar_caminhoes_por_tracao(tracao_busca):
    caminhoes = carregar_caminhoes()

    filtrados = []

    for c in caminhoes:
        if not c.get("ativo", True):
            continue

        if c.get("tracao") == tracao_busca:
            nome = f"{c.get('marca', '')} {c.get('modelo', '')} {c.get('ano', '')}".strip()
            if nome:
                filtrados.append(nome)

    return filtrados


def obter_entre_eixo_caminhao_em_foco(mensagem_cliente):
    caminhoes = carregar_caminhoes()
    texto = mensagem_cliente.lower()

    for c in caminhoes:
        if not c.get("ativo", True):
            continue

        nome = f"{c.get('marca', '')} {c.get('modelo', '')} {c.get('ano', '')}".strip().lower()

        if nome and nome in texto:
            return {
                "nome": nome,
                "entreEixo": c.get("entreEixo")
            }

    return None

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

VARIAÇÃO DE AFIRMAÇÕES:

Evite repetir sempre as mesmas expressões como:
- "Tenho sim, patrão"

Alterne naturalmente com:
- "Tem sim"
- "Esse tem"
- "Esse é"
- "Dá sim"

Sempre mantendo o tom humano e simples.


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

LINGUAGEM DE CAMINHONEIRO (REGRA):

Considere como equivalentes:
- toco = 4x2
- truck = 6x2
- traçado = 6x4

Nunca negar disponibilidade apenas por diferença de termo.
Sempre interpretar a linguagem do cliente de forma prática.


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


VALOR (REGRA IMPORTANTE):

Perguntar valor NÃO é intenção de compra imediata.

Quando o cliente perguntar preço ou valor:
- Responda o valor se ele estiver disponível
- Explique que é repasse
- NÃO transfira para o Gabriel
- NÃO peça nome
- NÃO conduza para fechamento

Transferência só deve ocorrer quando houver:
- pedido de negociação
- financiamento
- intenção clara de compra


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


MÚLTIPLAS INTENÇÕES NA MESMA FRASE:

Se o cliente fizer mais de um pedido na mesma mensagem
(ex: valor + foto, valor + informação):

- Responda TODOS os pedidos
- Em mensagens curtas, separadas
- Mantendo ordem natural da conversa

Nunca ignore parte da pergunta.

CONTEXTO JÁ DEFINIDO (REGRA CRÍTICA):

Se o cliente JÁ informou:
- qual caminhão quer
- ou o caminhão está claro no contexto da conversa

NUNCA:
- perguntar novamente qual caminhão é
- pedir confirmação desnecessária
- reiniciar o assunto

Sempre:
- seguir a conversa normalmente
- responder direto ao que o cliente pediu

Exemplo correto:
Cliente: "daf 460 2019 quero foto"
Resposta: "Com certeza, patrão. Já te mando as fotos."

Exemplo proibido:
"Só me confirma qual caminhão você quer ver?"

CONFIRMAÇÕES CURTAS (REGRA):

Respostas curtas do cliente como:
- "sim"
- "isso"
- "isso mesmo"
- "ok"
- "pode mandar"

Devem ser interpretadas como CONTINUIDADE da conversa,
e NÃO como uma nova intenção.

NUNCA:
- mudar de assunto
- reiniciar perguntas
- voltar etapas já concluídas

Sempre:
- seguir o fluxo atual naturalmente


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


AJUSTE DE FRASE (REGRA DE LINGUAGEM):

Evite usar expressões como:
- "jogando conversa fora"

Quando quiser conduzir a conversa de forma leve, use:
- "tá procurando caminhão ou só pesquisando?"

Essa frase deve ser priorizada no atendimento inicial.



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


FOTOS E VÍDEOS (REGRA ABSOLUTA):

Quando o cliente pedir fotos ou vídeos:

- Se o caminhão já estiver claro na conversa:
  NUNCA perguntar novamente qual caminhão é
  NUNCA pedir confirmação
  Apenas confirmar e avisar que vai mandar

Resposta padrão:
"Com certeza, patrão. Já te mando."

- Só perguntar qual caminhão é
  se realmente NÃO houver nenhuma referência clara antes


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


import re

def limpar_texto_whatsapp(texto):
    # Remove excesso de vírgulas
    texto = re.sub(r",\s*,+", ", ", texto)
    texto = re.sub(r"\s+,", ",", texto)

    # Evita frases longas com várias vírgulas
    texto = texto.replace(", e ", ". ")
    texto = texto.replace(", mas ", ". ")
    texto = texto.replace(", porque ", ". ")

    return texto.strip()


import re

def normalizar_pontuacao(texto):
    import re

    texto = texto.strip()

    # Remove combinações erradas tipo "!.," ",." "!!"
    texto = re.sub(r'([!?.,]){2,}', r'\1', texto)

    # Remove vírgula ou ponto no FINAL da frase
    texto = re.sub(r'[.,]+$', '', texto)

    # Remove exclamação no final
    texto = re.sub(r'!$', '', texto)

    # Mantém interrogação se for pergunta
    # (não faz nada aqui, só garante que não remove)

    # Espaços duplicados
    texto = re.sub(r'\s{2,}', ' ', texto)

    return texto.strip()



def extrair_link(texto, data=None):
    # 1️⃣ Tenta extrair link do texto
    if texto:
        regex = r"(https?://[^\s]+)"
        match = re.search(regex, texto)
        if match:
            return match.group(1)

    # 2️⃣ Fallback: preview de anúncio do WhatsApp
    if data:
        preview_url = data.get("linkPreview", {}).get("canonicalUrl")
        if preview_url:
            return preview_url

    return None

def identificar_caminhao_por_texto(texto):
    caminhoes = carregar_caminhoes()
    texto_lower = texto.lower()

    for c in caminhoes:
        if not c.get("ativo", True):
            continue

        nome = f"{c.get('marca', '')} {c.get('modelo', '')} {c.get('ano', '')}".lower()

        if nome and nome in texto_lower:
            return c

    return None



def quebrar_em_mensagens(texto, max_frases=2):
    frases = re.split(r'(?<=[.?])\s+', texto)
    mensagens = []
    bloco = []

    for frase in frases:
        if not frase:
            continue

        bloco.append(frase)

        if len(bloco) >= max_frases:
            mensagens.append(" ".join(bloco).strip())
            bloco = []

    if bloco:
        mensagens.append(" ".join(bloco).strip())

    return mensagens


def remover_reapresentacao(texto):
    substituicoes = [
        "sou o ronaldo, do atendimento da rw caminhões",
        "sou o ronaldo do atendimento da rw caminhões",
        "sou o ronaldo",
        "aqui é o ronaldo",
        "ronaldo, da rw caminhões",
        "da rw caminhões"
    ]

    texto_lower = texto.lower()

    for s in substituicoes:
        if s in texto_lower:
            idx = texto_lower.find(s)
            texto = texto[:idx] + texto[idx + len(s):]
            texto_lower = texto.lower()

    return texto.strip(" ,.-\n")


def obter_tracao_caminhao_em_foco(mensagem_cliente):
    caminhoes = carregar_caminhoes()
    texto = mensagem_cliente.lower()

    for c in caminhoes:
        if not c.get("ativo", True):
            continue

        nome = f"{c.get('marca', '')} {c.get('modelo', '')} {c.get('ano', '')}".strip().lower()

        if nome and nome in texto:
            return {
                "nome": nome,
                "tracao": c.get("tracao")
            }

    return None


MAPA_TRACAO = {
    "toco": "4x2",
    "4x2": "4x2",
    "truck": "6x2",
    "6x2": "6x2",
    "traçado": "6x4",
    "tracado": "6x4",
    "6x4": "6x4"
}


def processar_mensagem(mensagem_cliente, numero_cliente="desconhecido", data=None):
    user_lower = mensagem_cliente.lower()

    # =====================================================
    # CRIA SESSÃO
    # =====================================================
    if numero_cliente not in SESSOES:
        ajuste = carregar_prompt()
        system_prompt = PROMPT_BASE + ("\n\nAJUSTE TEMPORÁRIO:\n" + ajuste if ajuste else "")

        SESSOES[numero_cliente] = {
            "historico": [{"role": "system", "content": system_prompt}],
            "primeira_resposta": True,
            "ultima_mensagem_cliente": datetime.now(),
            "remarketing_enviado": False,
            "pausado_para_gabriel": False,
            "aguardando_nome": False,
            "nome_cliente": None,
            "resumo_para_gabriel": [],
            "caminhao_em_foco": None
        }

    sessao = SESSOES[numero_cliente]

    if sessao["pausado_para_gabriel"]:
        return None

    sessao["ultima_mensagem_cliente"] = datetime.now()
    sessao["remarketing_enviado"] = False

    # =====================================================
    # DETECTA SAUDAÇÃO
    # =====================================================
    cliente_saudou = any(
        s in user_lower for s in [
            "bom dia", "boa tarde", "boa noite", "opa", "fala", "e ai", "e aí", "oi", "olá"
        ]
    )

    def aplicar_saudacao(texto):
        texto = texto.strip()

        if sessao["primeira_resposta"]:
            sessao["primeira_resposta"] = False

            if cliente_saudou:
                return texto

            saudacao = "Fala, tudo bem? Aqui é o Ronaldo, da RW Caminhões."
            while texto and texto[0] in [",", ".", "!", " "]:
                texto = texto[1:].lstrip()

            return f"{saudacao} {texto}" if texto else saudacao

        return texto

    # =====================================================
    # IDENTIFICA CAMINHÃO EM FOCO
    # =====================================================
    if not sessao["caminhao_em_foco"]:
        caminhao = identificar_caminhao_por_texto(mensagem_cliente)
        if caminhao:
            sessao["caminhao_em_foco"] = caminhao

    # =====================================================
    # TOCO / TRUCK / TRAÇADO
    # =====================================================
    for palavra, tracao in MAPA_TRACAO.items():
        if palavra in user_lower:
            caminhao = sessao.get("caminhao_em_foco")

            if caminhao:
                if caminhao.get("tracao") == tracao:
                    return aplicar_saudacao(
                        f"Tenho sim, patrão. Esse é {tracao}, bem alinhado pra proposta de repasse"
                    )

                return aplicar_saudacao(
                    f"Esse específico não é {palavra}, mas sempre entra opção assim. "
                    "Vou te mandar o link do meu grupo pra acompanhar"
                )

            opcoes = filtrar_caminhoes_por_tracao(tracao)

            if opcoes:
                return aplicar_saudacao(
                    f"Tenho sim, patrão. Hoje tenho: {', '.join(opcoes)}"
                )

            return aplicar_saudacao(
                f"No momento não tenho {palavra} disponível, "
                "mas sempre entra coisa boa. Vou te mandar o link do meu grupo pra acompanhar"
            )

    # =====================================================
    # PEDIDO DE FOTOS
    # =====================================================
    if any(p in user_lower for p in ["foto", "fotos", "imagem", "imagens"]):
        caminhao = sessao.get("caminhao_em_foco")

        if caminhao:
            if caminhao.get("imagens"):
                enviar_imagens_caminhao(
                    numero_cliente,
                    caminhao["imagens"],
                    limite=3
                )
                return aplicar_saudacao("Com certeza, patrão. Já te mando as fotos")

            return aplicar_saudacao(
                "Consigo sim, patrão. Só estou conferindo as fotos certinho e já te mando"
            )

        return aplicar_saudacao(
            "Consigo sim, patrão. Só me confirma qual caminhão você quer ver"
        )

    # =====================================================
    # VALOR
    # =====================================================
    if any(v in user_lower for v in ["valor", "preço", "quanto", "custa"]):
        caminhao = sessao.get("caminhao_em_foco")

        if caminhao and caminhao.get("valor"):
            return aplicar_saudacao(
                f"Esse tá por R$ {caminhao['valor']}. Caminhão de repasse direto, sem maquiagem"
            )

        return aplicar_saudacao(
            "Esse valor eu prefiro confirmar certinho pra não te falar errado. Já confiro pra você"
        )

    # =====================================================
    # INTERESSE EM FECHAR
    # =====================================================
    if any(i in user_lower for i in ["quero fechar", "vamos fechar", "quero comprar"]):
        sessao["aguardando_nome"] = True
        sessao["resumo_para_gabriel"].append(f"Interesse em fechar: {mensagem_cliente}")
        return aplicar_saudacao(
            "Perfeito, patrão. Só pra eu te apresentar certinho pro Gabriel, qual é teu nome?"
        )

    # =====================================================
    # NEGOCIAÇÃO
    # =====================================================
    if any(n in user_lower for n in ["desconto", "negocia", "melhora o preço", "faz por menos"]):
        sessao["aguardando_nome"] = True
        sessao["resumo_para_gabriel"].append(f"Pedido de negociação: {mensagem_cliente}")
        return aplicar_saudacao(
            "Entendo, patrão. Isso eu prefiro alinhar direto com o Gabriel. Qual é teu nome?"
        )

    # =====================================================
    # GPT (FALLBACK)
    # =====================================================
    historico = sessao["historico"]
    historico.append({"role": "user", "content": mensagem_cliente})

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico,
        temperature=0.2
    )

    mensagem = resposta.choices[0].message.content.strip()
    mensagem = remover_reapresentacao(mensagem)
    mensagem = limpar_texto_whatsapp(mensagem)
    mensagem = normalizar_pontuacao(mensagem)
    mensagem = aplicar_saudacao(mensagem)

    historico.append({"role": "assistant", "content": mensagem})

    return quebrar_em_mensagens(mensagem)


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

        if not msg_id:
            return "OK", 200

        if msg_id in ULTIMAS_MENSAGENS:
            return "OK", 200

        ULTIMAS_MENSAGENS.append(msg_id)

        if data.get("type") != "ReceivedCallback":
            return "OK", 200

        if data.get("fromMe") is True:
            return "OK", 200

        numero = data.get("phone")

        texto = None

        # ========= TEXTO =========
        if isinstance(data.get("text"), dict):
            texto = data.get("text", {}).get("message")
        elif isinstance(data.get("text"), str):
            texto = data.get("text")

        if not texto:
            texto = data.get("body") or data.get("message") or data.get("caption")

        # ========= ÁUDIO =========
        if not texto and data.get("audio"):
            audio_url = data.get("audio", {}).get("audioUrl")

            if audio_url:
                try:
                    audio_path = f"/tmp/{msg_id}.ogg"
                    r = requests.get(audio_url, timeout=10)

                    with open(audio_path, "wb") as f:
                        f.write(r.content)

                    texto = transcrever_audio(audio_path)

                except Exception as e:
                    print("Erro ao baixar/transcrever áudio:", e)

        # ========= FALLBACK DE ÁUDIO =========
        if not texto:
            enviar_mensagem(
                numero,
                "Patrão, não consegui entender muito bem o áudio. "
                "Se puder, me manda de novo ou escreve aqui rapidinho."
            )
            return "OK", 200

        print(f">> Cliente {numero}: {texto}")

        respostas = processar_mensagem(texto, numero, data)


        # 🔕 Se a conversa foi transferida, nunca mais responder
        if respostas is None:
            return "OK", 200


        if isinstance(respostas, str):
            respostas = [respostas]

        for i, msg in enumerate(respostas):
            enviar_digitando(numero)
            enviar_mensagem(numero, msg)

            # Delay de 15s entre mensagens
            if i < len(respostas) - 1:
                time.sleep(5)



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

        # Nunca faz remarketing se já foi transferido
        if sessao.get("pausado_para_gabriel"):
            continue


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
