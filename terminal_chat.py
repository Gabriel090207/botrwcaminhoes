from bot_core.core import processar_mensagem
from bot_core.audio import transcrever_audio

print("🤖 BOT TERMINAL INICIADO")
print("Digite 'sair' para encerrar")
print("Para testar áudio: /audio audios/teste.ogg")

sessao = {
    "primeira_resposta": True,
    "caminhao_em_foco": None
}

while True:

    try:
        texto = input("\nCliente> ").strip()

        if texto.lower() == "sair":
            break

        # =========================
        # TESTE AUDIO
        # =========================
        if texto.startswith("/audio"):

            caminho = texto.replace("/audio", "").strip()

            print("🎧 Transcrevendo áudio...")

            texto_transcrito = transcrever_audio(caminho)

            if not texto_transcrito:
                print("Bot> Patrão, não consegui entender o áudio.")
                continue

            print("📝 Transcrição:", texto_transcrito)

            texto = texto_transcrito


        # =========================
        # PROCESSAR
        # =========================
        resultado = processar_mensagem(sessao, texto)

        if not resultado:
            print("Bot> (sem resposta)")
            continue


        # =========================
        # TEXTO
        # =========================
        reply = resultado.get("reply_text")

        if isinstance(reply, list):
            for r in reply:
                print("Bot>", r)
        else:
            print("Bot>", reply)


        # =========================
        # IMAGENS
        # =========================
        if resultado.get("action") == "send_images":
            print("Bot> 📸 Simulando envio de imagens:", len(resultado.get("images", [])))


        # =========================
        # ATUALIZA SESSÃO
        # =========================
        sessao["caminhao_em_foco"] = resultado.get("caminhao_em_foco")

    except KeyboardInterrupt:
        print("\nEncerrando...")
        break
