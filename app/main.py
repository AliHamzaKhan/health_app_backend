# import asyncio
from PIL import Image
# import psycopg2
#
# from app.db.database_connection import Database
# from app.db.db_query import DBQuery
# from app.models.ai_request_enum import AiRequestType
# from app.models.data_process import DataProcess
# from app.models.user_profile import UserProfile


from fastapi import FastAPI
from app.api.api_routes import router
from app.ai.my_gemini import MyGemini
from app.ai.my_openai import MyOpenAI

from app.models.ai_request_enum import AiRequestType

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.include_router(router)

# def main():
#     # image_url = 'https://imgv2-1-f.scribdassets.com/img/document/546218008/original/5455ac7f13/1725450237?v=1'
#     image_url = '/Users/aliawan/AndroidStudioProjects/health_app_backend/cbc_test.webp'
#     # response = requests.get(image_url)
#
#     # image_path = '/Users/aliawan/AndroidStudioProjects/health_app_backend/cbc_test.webp'
#
#     # Load the image using PIL
#     try:
#         with open(image_url, 'rb') as image_file:
#             img = Image.open(image_file)  # Open image using PIL.Image
#
#         # Create an instance of MyGemini and process the image
#         gemini = MyGemini()
#         gemini.generate_ai(AiRequestType.ECG_Report, img)
#
#
#         my_open_ai = MyOpenAI()
#         my_open_ai.generate_ai(AiRequestType.ECG_Report, img)
#
#     except FileNotFoundError:
#         print(f"File not found: {image_url}")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#
# if __name__ == "__main__":
#     import os
#     print(os.getcwd())
#     main()
