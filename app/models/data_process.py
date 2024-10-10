from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict
from app.models.ai_generated_text import AiGeneratedText
from app.models.ai_request_enum import AiRequestType


class DataProcess(BaseModel):
    id: str
    user_id: str
    prompt: str
    image_url: str
    token_used: int
    ai_generated_text: AiGeneratedText
    request_type : AiRequestType
    created_at : datetime


class DataProcessRequest(BaseModel):
    user_id: str
    prompt: str
    image_url: str
    token_used : int
    ai_generated_text: AiGeneratedText
    request_type : AiRequestType




