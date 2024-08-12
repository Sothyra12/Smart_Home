from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, date

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)    

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    user_type: str

    class Config:
        orm_mode = True

class UserInDBBase(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: str

class UserCreateWithPassword(UserCreate):
    password_hash: str    

class UserMinimal(BaseModel):
    username: str
    email: str
    user_id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenWithUser(Token):
    user: UserMinimal



class CombinedUserProfileUpdate(BaseModel):
    # Fields from users table
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[str] = None
    password: Optional[str] = None

    # Fields from user_profiles table
    full_name: Optional[str] = None
    birth_date: Optional[date] = None

    @field_validator('user_type')
    def validate_user_type(cls, v):
        if v is not None and v not in ['Tech Enthusiast', 'Remote Manager', 'Eco-Conscious User', 'Family Oriented', 'Administrator']:
            raise ValueError('Invalid user type')
        return v

class CombinedUserProfileResponse(BaseModel):
    # Fields from users table
    user_id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    user_type: str

    # Fields from user_profiles table
    #full_name: str
    # birth_date: date

    class Config:
        orm_mode = True 

class EnergyUsage(BaseModel):
    id: int
    device_id: int
    start_time: datetime
    end_time: datetime
    consumption: float
    timestamp: datetime


class UserSettings(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    setting_key: str
    setting_value: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserSettingsCreate(BaseModel):
    setting_key: str
    setting_value: str

    class Config:
        schema_extra = {
            "example": {
                "setting_key": "leave_home_office",
                "setting_value": "low_energy_mode",
            }
        }