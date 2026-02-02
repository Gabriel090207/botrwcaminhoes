from fastapi import FastAPI

app = FastAPI(title="Bot Caminhões API")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "backend funcionando"}


from backend.app.bot.brain import generate_reply


@app.post("/bot/message")
def bot_message(data: dict):
    user_message = data.get("message", "")

    reply = generate_reply(user_message)

    return {
        "reply": reply
    }
