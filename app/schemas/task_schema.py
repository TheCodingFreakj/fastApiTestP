from pydantic import BaseModel
from typing import List
from datetime import datetime
class ItemResponse(BaseModel):
    batchid: str
    response: List[int]
    status: str
    started_at: datetime
    end_at: datetime

class ItemInput(BaseModel):
    batchid: str
    payload: List