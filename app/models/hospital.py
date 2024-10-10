from typing import Optional, List
from pydantic import BaseModel
from app.models.rating import Rating


class Hospital(BaseModel):
    id: str
    name: str
    address: str
    phone_number: str
    email: str
    website: Optional[str] = None
    type: Optional[str] = None
    departments: Optional[List[str]] = None
    rating: List[Rating]
    latlng: Optional[str] = None
    img: Optional[str] = None
    staff_count: Optional[int] = None




class HospitalRequest(BaseModel):
    name: str
    address: str
    phone_number: str
    email: str
    website: Optional[str] = None
    type: Optional[str] = None
    departments: Optional[List[str]] = None
    rating: List[Rating]
    latlng: Optional[str] = None
    img: Optional[str] = None
    staff_count: Optional[int] = None

# hospital = Hospital(
#     id="1",
#     name="City General Hospital",
#     address="456 Main St, Cityville",
#     phone_number="987-654-3210",
#     email="info@cityhospital.com",
#     website="http://cityhospital.com",
#     type="General",
#     departments=["Cardiology", "Pediatrics", "Neurology"],
#     rating=[Rating(id='', userId='', comments='', rating=1.0), Rating(id='', userId='', comments='', rating=1.0)],
#     latlng="40.7128,-74.0060",  # Example coordinates
#     img="http://cityhospital.com/logo.png"  # URL of the hospital logo
# )
