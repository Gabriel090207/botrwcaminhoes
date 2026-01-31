import os
from openai import OpenAI

_client = None


def _get_client() -> OpenAI:
    global _client

    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY não configurada. "
                "Cria um .env e coloca OPENAI_API_KEY=xxxx"
            )

        _client = OpenAI(api_key=api_key)

    return _client


def transcrever_audio(caminho_audio: str) -> str | None:
    """
    Transcreve áudio (ogg, mp3, wav).
    Retorna texto ou None.
    """

    try:
        client = _get_client()

        with open(caminho_audio, "rb") as f:
            resp = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=f
            )

        texto = (resp.text or "").strip()

        if not texto:
            return None

        return texto

    except Exception as e:
        print("Erro transcrevendo áudio:", e)
        return None
