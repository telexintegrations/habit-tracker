from pydantic import BaseModel
from typing import List

class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str

class TickPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]