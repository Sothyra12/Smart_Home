from pydantic import BaseModel
from typing import List, Optional

class DeviceBase(BaseModel):
    name: str
    type: Optional[str] = None
    image: Optional[str] = None
    is_on: Optional[bool] = False
    power_rating: Optional[float] = 0.0
    room_id: Optional[int] = None
    user_id: Optional[int] = None

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
