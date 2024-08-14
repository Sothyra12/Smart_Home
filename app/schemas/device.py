from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    type: Optional[str] = None
    image: Optional[str] = None
    is_on: Optional[bool] = False
    power_rating: Optional[float] = 0.0
    room_id: Optional[int] = None
    user_id: Optional[int] = None
    brand: Optional[str] = None
    model_number: Optional[str] = None
    energy_limit: Optional[float] = 0.0

class DeviceCreate(DeviceBase):
    pass

class Device(DeviceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class DeviceConsumptionBase(BaseModel):
    device_id: int
    start_time: datetime
    end_time: datetime
    consumption: float

class DeviceConsumptionCreate(DeviceConsumptionBase):
    device_id: int

class DeviceConsumption(DeviceConsumptionBase):
    id: int
    # timestamp: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True     

class DeviceUpdate(BaseModel):
    energy_limit: float


# New Schema
class DeviceWithConsumption(DeviceBase):
    latest_consumption: Optional[float] = None
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str