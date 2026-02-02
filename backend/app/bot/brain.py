def generate_reply(message: str) -> str:
    if not message or not message.strip():
        return "Pode me enviar sua mensagem novamente?"

    msg = message.lower()

    # Saudação
    if any(word in msg for word in ["oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"]):
        return "Olá! Posso ajudar a encontrar caminhões disponíveis."

    # Pergunta sobre disponibilidade
    if any(word in msg for word in ["caminhão", "caminhao", "disponível", "disponivel"]):
        return "Vou verificar os caminhões disponíveis para você."

    # fallback
    return "Certo! Pode me dar mais detalhes do que precisa?"
