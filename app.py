from flask import Flask, request, jsonify
from bot_core.core import processar_mensagem

app = Flask(__name__)

sessoes = {}

@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    numero = data.get("phone")
    texto = data.get("text", {}).get("message")

    if not numero or not texto:
        return jsonify({"status": "ignored"})

    if numero not in sessoes:
        sessoes[numero] = {
            "primeira_resposta": True,
            "caminhao_em_foco": None
        }

    sessao = sessoes[numero]

    resultado = processar_mensagem(sessao, texto)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
