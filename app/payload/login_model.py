from typing import Optional
from pydantic import BaseModel


class LoginModel(BaseModel):
    user_type_id: Optional[int]
    phone_number: Optional[str]
    email: Optional[str]
    fcm_token: Optional[str]


    class Config:
        extra = "forbid"
