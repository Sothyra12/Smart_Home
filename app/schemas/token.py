from typing import Optional
from pydantic import BaseModel
from app.schemas.user import UserMinimal  

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserMinimal

class TokenPayload(BaseModel):
    sub: Optional[int] = None