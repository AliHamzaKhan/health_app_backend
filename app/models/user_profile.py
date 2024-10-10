from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    id: Optional[str] = None  # Allow id to be optional
    first_name: str
    last_name: str
    email: str
    phone_no: str
    dob: str
    country: str
    city: str
    gender: str
    profile_image: str
    is_verified: bool
    package_id: int
    usage: float
    user_type_id: int


class UserProfileRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_no: str
    dob: str
    country: str
    city: str
    gender: str
    profile_image: str
    is_verified: bool
    package_id: int
    usage: float
    user_type_id: int
