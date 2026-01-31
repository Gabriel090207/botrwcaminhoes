from firebase_caminhoes import carregar_caminhoes
from firebase_service import carregar_prompt  # ajuste dinâmico (se tiver)
from bot_core.constants import GRUPO_LINK


def _gerar_contexto_caminhoes() -> str:
    caminhoes = carregar_caminhoes() or []
    ativos = [c for c in caminhoes if c.get("ativo", True)]

    if not ativos:
        return "Nenhum caminhão disponível no momento."

    blocos = []
    for c in ativos:
        bloco = (
            f"- Marca: {c.get('marca', 'Não informado')}\n"
            f"  Modelo: {c.get('modelo', 'Não informado')}\n"
            f"  Ano: {c.get('ano', 'Não informado')}\n"
            f"  Tração: {c.get('tracao', 'Não informado')}\n"
            f"  Valor: {c.get('valor', 'Não informado')}\n"
            f"  Observação: {c.get('observacao', 'Repasse direto')}\n"
        )
        blocos.append(bloco)

    return "\n".join(blocos)


def gerar_prompt_completo() -> str:
    prompt_base = """
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

ESTILO:
- Atendimento humano
- Mensagens curtas
- Nada robótico

REGRAS IMPORTANTES:
- Nunca usar markdown (nada de [texto](link))
- Quando mandar o grupo, mandar o link PURO:
""" + GRUPO_LINK + """

CAMINHÕES DISPONÍVEIS:
- O sistema controla os caminhões.
- Nunca invente caminhão.
- Só fale de caminhão se tiver na base.
"""

    ajuste = carregar_prompt()
    if ajuste:
        prompt_base += "\n\nAJUSTE TEMPORÁRIO:\n" + ajuste

    contexto = _gerar_contexto_caminhoes()

    prompt_final = (
        prompt_base
        + "\n\nBASE DE CAMINHÕES DO SISTEMA (ATUALIZADA):\n"
        + contexto
        + "\n\nINSTRUÇÃO FINAL:\n"
        + "Responda sempre como humano no WhatsApp, curto e direto."
    )

    return prompt_final
