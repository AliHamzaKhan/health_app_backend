from typing import Optional

from openai import BaseModel


class LoginModel(BaseModel):
    user_type_id: Optional[int]
    phone_number: Optional[str]
    email: Optional[str]

    class Config:
        extra = "forbid"
