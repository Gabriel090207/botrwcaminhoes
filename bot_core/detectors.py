import re
from bot_core.utils import normalizar_texto

PALAVRAS_FOTO = ["foto", "fotos", "imagem", "imagens", "vídeo", "video", "videos", "vídeos"]

MAPA_TRACAO = {
    "toco": "4x2",
    "4x2": "4x2",
    "truck": "6x2",
    "trucado": "6x2",
    "6x2": "6x2",
    "traçado": "6x4",
    "tracado": "6x4",
    "6x4": "6x4",
    "bitruck": "8x2",
    "8x2": "8x2",
}

def detectar_pedido_foto(texto: str) -> bool:
    t = normalizar_texto(texto)
    return any(p in t for p in PALAVRAS_FOTO)

def detectar_tracao_pedida(texto: str) -> str | None:
    t = normalizar_texto(texto)
    for palavra, tracao in MAPA_TRACAO.items():
        if palavra in t:
            return tracao
    return None

def extrair_ano(texto: str) -> int | None:
    t = normalizar_texto(texto)
    m = re.search(r"(19\d{2}|20\d{2})", t)
    if not m:
        return None
    try:
        return int(m.group(1))
    except:
        return None

def extrair_numeros(texto: str) -> set[str]:
    return set(re.findall(r"\b\d{3}\b|\b\d{4}\b", normalizar_texto(texto)))

def detectar_marca(texto: str) -> str | None:
    t = normalizar_texto(texto)
    marcas = ["daf", "volvo", "scania", "mercedes", "mb", "iveco", "man", "vw", "volks", "ford"]
    for m in marcas:
        if re.search(rf"\b{re.escape(m)}\b", t):
            return "mercedes" if m in ["mb"] else ("volkswagen" if m in ["vw", "volks"] else m)
    return None

def score_caminhao(texto: str, caminhao: dict) -> int:
    """
    Pontua caminhão vs texto do cliente.
    Evita o bug do 510 cair no 460.
    """
    t = normalizar_texto(texto)
    pts = 0

    marca = (caminhao.get("marca") or "").strip().lower()
    modelo = (caminhao.get("modelo") or "").strip().lower()
    ano = str(caminhao.get("ano") or "").strip()
    tracao = (caminhao.get("tracao") or "").strip().lower()

    # marca
    if marca and marca in t:
        pts += 3

    # tração (direto ou apelido)
    if tracao and tracao in t:
        pts += 2
    else:
        for apelido, tr in MAPA_TRACAO.items():
            if apelido in t and tr == tracao:
                pts += 2
                break

    # ano
    if ano and ano in t:
        pts += 3

    # números do modelo (ex: 460, 510, 461)
    nums_texto = extrair_numeros(t)

    # pega números do modelo
    nums_modelo = set(re.findall(r"\b\d{3}\b|\b\d{4}\b", modelo))

    # se cliente falou 510, e modelo tem 510, ganha muito
    inter = nums_texto.intersection(nums_modelo)
    if inter:
        pts += 6

    # também ajuda se cliente falou "xf", "fh" etc
    tokens_modelo = set(re.findall(r"[a-z]{2,}", modelo))
    for tok in tokens_modelo:
        if tok in t:
            pts += 1

    return pts

def detectar_caminhao_no_texto(texto: str, caminhoes_base: list[dict]) -> dict | None:
    if not texto or not caminhoes_base:
        return None

    melhores = []
    for c in caminhoes_base:
        if not c.get("ativo", True):
            continue
        pts = score_caminhao(texto, c)
        if pts > 0:
            melhores.append((pts, c))

    if not melhores:
        return None

    melhores.sort(key=lambda x: x[0], reverse=True)
    top_pts, top_c = melhores[0]

    # threshold mínimo pra “cravar”
    return top_c if top_pts >= 6 else None
