import base64
from http.client import responses
from pyexpat.errors import messages
import io
from typing import Tuple

from PIL import Image
import openai
from app.constant.prompts import Prompts
from app.constant.utils import parse_gemini_response
from app.keys.my_keys import OPENAI_API_KEY
from app.models.ai_request_enum import AiRequestType
from app.models.data_process import AiGeneratedText


class MyOpenAI:
    def __init__(self):
        self.api_key = OPENAI_API_KEY
        self.model_name = "gpt-3.5-turbo"

    def generate_ai(self, ai_request_type: AiRequestType, image: Image.Image) -> Tuple[AiGeneratedText, str]:
        openai.api_key = self.api_key
        try:
            prompt = Prompts(ai_request_type)
            with io.BytesIO() as img_buffer:
                image.save(img_buffer, format="PNG")  # Save the image to a bytes buffer
                img_buffer.seek(0)  # Move the pointer to the start of the buffer
                image_data = img_buffer.getvalue()

            base64_image = base64.b64encode(image_data).decode('utf-8')
            full_prompt = f"{prompt}\n\n![Image](data:image/png;base64,{base64_image})"  # Include the image in markdown format

            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": full_prompt}]
                # messages=[{"role": "user", "content": prompt}],
                # files=[{"file": ("image.png", image_data, "image/png")}]
            )
            ai_generated_text, formatted_response = parse_gemini_response(response['choices'][0]['message']['content'])
            token_used = response['usage']['total_tokens']
            return ai_generated_text, formatted_response, token_used
        except Exception as e:
            print(f"Error while calling OpenAI API: {str(e)}")
            return "Error occurred while generating AI content."
