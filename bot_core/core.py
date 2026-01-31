from firebase_caminhoes import carregar_caminhoes
from bot_core.detectors import detectar_caminhao_no_texto, detectar_tracao_pedida
from bot_core.intent import detectar_intencao
from bot_core.humanizer import afirmar, continuar


GRUPO_LINK = "https://chat.whatsapp.com/F69FL3ligTJGPRAJfKsQaW?mode=gi_t"


# =========================================================
# FORMATAR VALOR CORRETO
# =========================================================
def formatar_valor(valor_raw):

    try:
        valor = float(str(valor_raw).replace(",", "."))
    except:
        return None

    if valor > 1000000:
        valor = valor / 100

    mil = int(valor / 1000)

    if mil >= 1000:
        return "1 milhão"

    return f"{mil} mil"


# =========================================================
# RESPOSTA PADRÃO
# =========================================================
def resposta(textos, action="text", imagens=None, caminhao=None):

    if isinstance(textos, str):
        textos = [textos]

    return {
        "reply_text": textos,
        "action": action,
        "images": imagens or [],
        "caminhao_em_foco": caminhao
    }


# =========================================================
# PROCESSAMENTO PRINCIPAL
# =========================================================
def processar_mensagem(sessao, texto):

    caminhoes = carregar_caminhoes() or []

    if not texto:
        return resposta("Me manda de novo que não entendi direito.", caminhao=sessao.get("caminhao_em_foco"))

    texto_lower = texto.lower()

    intencao = detectar_intencao(texto_lower)

    caminhao_em_foco = sessao.get("caminhao_em_foco")

    # =====================================================
    # PRIMEIRA RESPOSTA
    # =====================================================
    if sessao.get("primeira_resposta"):

        sessao["primeira_resposta"] = False

        detectado_primeira = detectar_caminhao_no_texto(texto_lower, caminhoes)

        if detectado_primeira:
            caminhao_em_foco = detectado_primeira

            nome = f"{caminhao_em_foco.get('marca')} {caminhao_em_foco.get('modelo')} {caminhao_em_foco.get('ano')}"

            return resposta([
                "Ôpa! Aqui é o Ronaldo, da RW Caminhões.",
                f"{afirmar()} {nome}."
            ], caminhao=caminhao_em_foco)

        return resposta([
            "Ôpa! Aqui é o Ronaldo, da RW Caminhões.",
            "Show.",
            "Tá procurando caminhão ou só pesquisando?"
        ])

    # =====================================================
    # DETECTAR CAMINHÃO
    # =====================================================
    detectado = detectar_caminhao_no_texto(texto_lower, caminhoes)

    if detectado:
        caminhao_em_foco = detectado

    # =====================================================
    # DETECTAR TRAÇÃO
    # =====================================================
    tracao = detectar_tracao_pedida(texto_lower)

    if tracao and not caminhao_em_foco:

        encontrados = [
            c for c in caminhoes
            if c.get("tracao") == tracao and c.get("ativo", True)
        ]

        if encontrados:
            caminhao_em_foco = encontrados[0]

    # =====================================================
    # INTENÇÃO VALOR
    # =====================================================
    if intencao == "valor" and caminhao_em_foco:

        valor_formatado = formatar_valor(caminhao_em_foco.get("valor"))

        if valor_formatado:
            return resposta([
                f"Ele tá na faixa de {valor_formatado}.",
                "É repasse direto."
            ], caminhao=caminhao_em_foco)

    # =====================================================
    # INTENÇÃO FOTO
    # =====================================================
    if intencao == "foto" and caminhao_em_foco:

        imagens = caminhao_em_foco.get("imagens") or []

        return resposta(
            "Com certeza, patrão. Já te mando.",
            action="images",
            imagens=imagens,
            caminhao=caminhao_em_foco
        )

    # =====================================================
    # INTENÇÃO TROCA
    # =====================================================
    if intencao == "troca":

        return resposta([
            "Patrão, nesses caminhões eu não consigo pegar troca não, são só pra venda.",
            "São caminhões de concessionária, transportadora ou cliente final.",
            f"Às vezes aparece algum que aceita troca, por isso vou te mandar o grupo:",
            GRUPO_LINK
        ], caminhao=caminhao_em_foco)

    # =====================================================
    # INTENÇÃO GRUPO
    # =====================================================
    if intencao == "grupo":

        return resposta([
            "Tem sim.",
            "Segue o link:",
            GRUPO_LINK
        ], caminhao=caminhao_em_foco)

    # =====================================================
    # INTENÇÃO REPASSE
    # =====================================================
    if intencao == "repasse":

        return resposta([
            "Repasse é caminhão direto do dono ou empresa.",
            "Sem maquiagem.",
            "Preço melhor."
        ], caminhao=caminhao_em_foco)

    # =====================================================
    # CAMINHÃO EM FOCO
    # =====================================================
    if caminhao_em_foco:

        nome = f"{caminhao_em_foco.get('marca')} {caminhao_em_foco.get('modelo')} {caminhao_em_foco.get('ano')}"
        resumo = caminhao_em_foco.get("resumo")

        if resumo:
            return resposta([
                f"{nome}.",
                resumo
            ], caminhao=caminhao_em_foco)

        return resposta([
            f"{afirmar()} {nome}.",
            continuar()
        ], caminhao=caminhao_em_foco)

    # =====================================================
    # FALLBACK
    # =====================================================
    return resposta("Me diz qual modelo você tá procurando que eu te falo certinho.")
