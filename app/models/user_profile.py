from pydantic import BaseModel
from typing import Optional


class UserProfile(BaseModel):
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    phone_no: str
    dob: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[str] = None
    profile_image: Optional[str] = None
    is_verified: bool
    package_id: int
    total_usage: float = 0.0
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
    total_usage: float
    user_type_id: int
