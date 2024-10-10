from msilib.schema import File

from fastapi import UploadFile
from pydantic import BaseModel

from app.models.ai_request_enum import AiRequestType


class ProcessDataPayloadModel(BaseModel):
    userId: str
    ai_request_type: AiRequestType
    image: UploadFile = File(...)