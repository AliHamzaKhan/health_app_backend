from typing import List, Optional

from pydantic import BaseModel

from app.models.rating import Rating


class Doctor(BaseModel):
    id: str
    name: str
    email: str
    degree: str
    age: str
    phone_no: str
    gender: str
    address: str
    hospitals: List[str]
    specialization: List[str]
    experience: str
    image: Optional[str] = None
    availability: Optional[str] = None


class DoctorRequest(BaseModel):
    name: str
    email: str
    degree: str
    age: str
    phone_no: str
    gender: str
    address: str
    hospitals: List[str]
    specialization: List[int]
    experience: str
    image: Optional[str] = None
    availability: Optional[str] = None



# doctor = Doctor(
#     id="1",
#     name="Dr. John Doe",
#     email="john.doe@example.com",
#     degree="MBBS",
#     age="35",
#     phone_no="123-456-7890",
#     gender="Male",
#     address="123 Main St, Cityville",
#     hospitals=["City Hospital", "Town Clinic"],
#     specialization="Cardiology",
#     experience=10,
#     image="http://example.com/profile.jpg",
#     availability="Mon-Fri: 9 AM - 5 PM",
#     rating=4.5
# )
