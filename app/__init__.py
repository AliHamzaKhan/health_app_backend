from fastapi import APIRouter, UploadFile, File, FastAPI
from app.db.database_connection import Database
from app.db.db_query import DBQuery
from app.models.ai_request_enum import AiRequestType
from app.models.data_process import DataProcess
from app.models.user_profile import UserProfile