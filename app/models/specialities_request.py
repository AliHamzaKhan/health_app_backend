from typing import List

from pydantic import BaseModel


class SpecialitiesRequest(BaseModel):
    data: List[str]