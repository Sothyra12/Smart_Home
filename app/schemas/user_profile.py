from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True