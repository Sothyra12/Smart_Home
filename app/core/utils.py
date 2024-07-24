# utils.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return decode_jwt(token)

def get_current_token(token: str = Depends(oauth2_scheme)):
    decode_jwt(token)
    return token
