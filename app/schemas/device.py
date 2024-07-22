from pydantic import BaseModel
from typing import List, Optional

class DeviceBase(BaseModel):
    name: str
    type: str
    image: Optional[str] = None  # New field for base64 encoded image

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    user_id: int
    room_id: Optional[int] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
