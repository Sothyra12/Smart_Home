from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SceneDeviceBase(BaseModel):
    is_on: bool
    settings: Optional[str] = None

class SceneDeviceCreate(SceneDeviceBase):
    device_id: int

class SceneDevice(SceneDeviceBase):
    id: int
    scene_id: int
    device_id: int

    class Config:
        orm_mode = True

class SceneBase(BaseModel):
    name: str

class SceneCreate(SceneBase):
    devices: List[SceneDeviceCreate]

class Scene(SceneBase):
    id: int
    user_id: int
    scene_devices: List[SceneDevice] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True