from bot_core.utils import normalizar_texto
from bot_core.detectors import extrair_ano

def detectar_intencao(texto: str):

    if not texto:
        return "normal"

    t = texto.lower()

    # VALOR
    if any(p in t for p in [
        "valor", "preço", "preco", "quanto", "tá quanto", "ta quanto"
    ]):
        return "valor"

    # FOTO
    if any(p in t for p in [
        "foto", "fotos", "imagem", "video", "vídeo"
    ]):
        return "foto"

    # TROCA / BRICK
    if any(p in t for p in [
        "troca", "brick", "permuta"
    ]):
        return "troca"

    # GRUPO
    if "grupo" in t:
        return "grupo"

    # DETALHES
    if any(p in t for p in [
        "detalhe", "detalhes", "mais info", "me fala mais", "me passa mais"
    ]):
        return "detalhes"

    # COMPRA / NEGOCIAÇÃO
    if any(p in t for p in [
        "quero comprar",
        "vamos fechar",
        "quero negociar",
        "aceita proposta",
        "faz negócio"
    ]):
        return "comprar"

    return "normal"
