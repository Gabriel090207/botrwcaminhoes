import random

def afirmar() -> str:
    return random.choice([
        "Tem sim.",
        "Esse tem sim.",
        "Tenho sim, patrão.",
        "Dá sim.",
    ])

def continuar() -> str:
    return random.choice([
        "Quer foto ou mais detalhe?",
        "Quer que eu te mande as fotos?",
        "Quer mais informação dele?",
    ])

def resposta_social(perguntar_de_volta: bool) -> str:
    base = random.choice([
        "Tudo tranquilo por aqui, graças a Deus.",
        "Tudo certo por aqui, graças a Deus.",
        "Tudo beleza por aqui.",
    ])
    if perguntar_de_volta:
        return base + " E por aí?"
    return base
