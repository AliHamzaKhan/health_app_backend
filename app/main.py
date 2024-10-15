
from fastapi import FastAPI
from app.api.api_routes import router


app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
app.include_router(router)


