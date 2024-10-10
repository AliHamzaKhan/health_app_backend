from datetime import datetime

from pydantic import BaseModel


class TokenUsed(BaseModel):
    id : str
    data_process_id : str
    user_id : str
    token_used : int
    created_at : datetime



class TokenUsedRequest(BaseModel):
    data_process_id : str
    user_id : str
    token_used : int
