from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from app.models.device import Device

class RoomBase(BaseModel):
    name: str
    image: Optional[str] = None  # New field for base64 encoded image

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    user_id: int
    devices: List[Device] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
