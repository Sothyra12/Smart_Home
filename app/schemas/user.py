from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

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
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)

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

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenWithUser(Token):
    user: UserMinimal