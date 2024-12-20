from typing import List
from pydantic import BaseModel


class AiGeneratedText(BaseModel):
    diagnosis: str
    treatment: str
    doctors_recommended: List[str]
    suggestions: List[str]
