from pydantic import BaseModel


class Rating(BaseModel):
    id : str
    user_id : str
    rating : float
    comment : str



class RatingRequest(BaseModel):
    user_id : str
    rating : float
    comment : str



class HospitalRatingRequest(BaseModel):
    user_id : str
    hospital_id : str
    rating: float
    comment: str

class HospitalRating(BaseModel):
    id : str
    user_id : str
    hospital_id : str
    rating: float
    comment: str


class DoctorRatingRequest(BaseModel):
    user_id : str
    doctor_id : str
    rating: float
    comment: str

class DoctorRating(BaseModel):
    id : str
    user_id : str
    doctor_id : str
    rating: float
    comment: str