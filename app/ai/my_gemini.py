import json
from typing import Tuple
import google.generativeai as genai
from google.generativeai import GenerativeModel
from google.generativeai.types.generation_types import GenerateContentResponse
from app.constant.prompts import Prompts
from app.constant.utils import parse_gemini_response
# from app.keys.my_keys import GEMINI_API_KEY
from app.models.ai_request_enum import AiRequestType
from PIL import Image
import os
from dotenv import load_dotenv
from app.models.data_process import AiGeneratedText



load_dotenv()
class MyGemini:

    def __init__(self,):
        GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
        genai.configure(api_key=GEMINI_API_KEY)
        print(GEMINI_API_KEY)
        self.model: GenerativeModel = genai.GenerativeModel("gemini-1.5-flash")



    def generate_ai(self, ai_request_type : AiRequestType, image: Image.Image) -> Tuple[AiGeneratedText, int]:
        prompt = Prompts(ai_request_type)
        response: GenerateContentResponse = self.model.generate_content([
            prompt.get_merged_prompt(),
            image
        ])
        print(f'response.text {response.text}')
        a = response.usage_metadata.prompt_token_count
        b = response.usage_metadata.candidates_token_count
        c = response.usage_metadata.cached_content_token_count

        ai_generated_text, formatted_response = parse_gemini_response(response.text)
        token_used = response.usage_metadata.total_token_count
        print(f'prompt_token_count {a} | candidates_token_count {b} | cached_content_token_count {c}')
        print(f'formatted_response {formatted_response}')
        print(f'token_used {token_used}')
        return ai_generated_text, token_used




