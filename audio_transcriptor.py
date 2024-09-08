import os

from dotenv import load_dotenv
from openai import OpenAI


class AudioTranscriptor:

    def __init__(self):

        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)

    def transcribe_with_whisper(self, audio_file_name):

        audio_file = open(audio_file_name, "rb")

        AI_generated_transcript = self.openai_client.audio.transcriptions.create(
            model="whisper-1", file=audio_file, language="tr"
        )

        return AI_generated_transcript.text
