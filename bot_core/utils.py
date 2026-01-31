import re

def normalizar_texto(t: str) -> str:
    return (t or "").strip().lower()

def quebrar_em_mensagens(texto: str, max_frases: int = 2) -> list[str]:
    """
    Quebra texto em mensagens curtas. WhatsApp gosta disso.
    """
    if not texto:
        return []

    texto = texto.strip()
    # Divide por pontuação final
    frases = re.split(r'(?<=[.!?])\s+', texto)
    msgs, bloco = [], []

    for f in frases:
        f = f.strip()
        if not f:
            continue
        bloco.append(f)
        if len(bloco) >= max_frases:
            msgs.append(" ".join(bloco))
            bloco = []

    if bloco:
        msgs.append(" ".join(bloco))

    return msgs

def formatar_valor(valor_raw):
    if not valor_raw:
        return None

    try:
        v = float(str(valor_raw).replace(",", "."))

        # Caso venha 31000000 → dividir por 100
        if v > 1000000:
            v = v / 100

        mil = int(v / 1000)

        if mil >= 1000:
            return f"{mil//1000} milhão"

        return f"{mil} mil"

    except:
        return None


def eh_so_saudacao(texto: str) -> bool:
    t = normalizar_texto(texto)
    if not t:
        return False

    # só saudação / cordialidade curtinha
    padroes = [
        "oi", "olá", "ola", "opa", "ôpa",
        "bom dia", "boa tarde", "boa noite",
        "e ai", "e aí", "tudo bem", "tudo certo"
    ]
    # se tiver coisa além disso, não é só saudação
    return any(t == p for p in padroes)

def contem_pergunta_como_voce(texto: str) -> bool:
    t = normalizar_texto(texto)
    return ("e vc" in t) or ("e voce" in t) or ("e você" in t)
