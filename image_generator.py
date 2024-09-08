import os
from datetime import datetime, timezone
from io import BytesIO

import google.generativeai as genai
import requests
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image


class ImageGenerator:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        genai.configure(api_key=self.google_api_key)

    def generate_image_with_dalle(self, prompt):
        AI_response = self.openai_client.images.generate(
            model="dall-e-2",
            size="1024x1024",
            quality="hd",
            n=1,
            response_format="url",
            prompt=prompt,
        )

        image_url = AI_response.data[0].url
        response = requests.get(image_url)
        image_bytes = BytesIO(response.content)

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"./img/generated_image_{timestamp}.png"

        if not os.path.exists("./img"):
            os.makedirs("./img")

        with open(filename, "wb") as file:
            file.write(image_bytes.getbuffer())

        return filename

    def image_and_prompt_with_gemini(self, image_path, prompt):
        multimodality_prompt = f"""
        I would like you to recreate the image I've provided, along with some additional instructions. 
        First, describe the image in great detail. Then, I will use the final text you provide to generate a visual using an AI model. 
        Keep in mind that the final version of your response will be used as a prompt for image generation.
        Here's the additional instruction: {prompt}
        """

        client = genai.GenerativeModel(model_name="gemini-pro-vision")
        source_image = Image.open(image_path)

        AI_response = client.generate_content([multimodality_prompt, source_image])
        AI_response.resolve()

        return AI_response.text

    def generate_image(self, image_path, prompt):
        generated_prompt = self.image_and_prompt_with_gemini(image_path, prompt)
        filename = self.generate_image_with_dalle(generated_prompt)
        return filename


# import os
# from datetime import datetime, timezone
# from io import BytesIO

# import google.generativeai as genai
# import requests
# from dotenv import load_dotenv
# from openai import OpenAI
# from PIL import Image

# load_dotenv()

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=OPENAI_API_KEY)
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)


# def generate_image_with_dalle(promt):

#     AI_response = client.images.generate(
#         model="dall-e-2",
#         size="1024x1024",
#         quality="hd",
#         n=1,
#         response_format="url",
#         prompt=promt,
#     )

#     image_url = AI_response.data[0].url
#     response = requests.get(image_url)
#     image_bytes = BytesIO(response.content)

#     timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")

#     filename = f"./img/generated_image_{timestamp}.png"

#     if not os.path.exists("./img"):
#         os.makedirs("./img")

#     # saved to local
#     with open(filename, "wb") as file:
#         file.write(image_bytes.getbuffer())

#     return filename


# def image_and_prompt_with_gemini(image_path, prompt):

#     multimodality_prompt = f"""
#     I would like you to recreate the image I’ve provided, along with some additional instructions.
#     First, describe the image in great detail. Then, I will use the final text you provide to generate a visual using an AI model.
#     Keep in mind that the final version of your response will be used as a prompt for image generation.
#     Here’s the additional instruction: {prompt}
#     """

#     client = genai.GenerativeModel(model_name="gemini-pro-vision")
#     source_image = Image.open(image_path)

#     AI_response = client.generate_content([multimodality_prompt, source_image])

#     AI_response.resolve()

#     return AI_response.text


# def generate_image(image_path, prompt):
#     generated_prompt = image_and_prompt_with_gemini(image_path, prompt)

#     filename = generate_image_with_dalle(generated_prompt)
#     return filename
