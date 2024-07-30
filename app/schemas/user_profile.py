from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserProfileBase(BaseModel):
    full_name: str
    birth_date: datetime

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True