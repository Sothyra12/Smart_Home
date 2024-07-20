# app/models/login.py

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    #grant_type: str
    password: str
