import asyncio

from fastapi import FastAPI
from app.api.api_routes import router, db, get_hospitals
from app.payload.login_model import LoginModel
import app.service.initialize_service as service

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.include_router(router)



async def main():
  await add_doctors()




if __name__ == "__main__":
    asyncio.run(main())