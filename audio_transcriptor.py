import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def transcribe_with_whisper(audio_file_name):

    audio_file = open(audio_file_name, "rb")

    AI_generated_transcript = client.audio.transcriptions.create(
        model="whisper-1", file=audio_file, language="tr"
    )

    return AI_generated_transcript.text
