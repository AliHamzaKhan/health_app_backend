from typing import Optional

from pydantic import BaseModel


class UsedTokenRequestPayload(BaseModel):
    user_id: str
    data_process_id: Optional[str] = None