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
