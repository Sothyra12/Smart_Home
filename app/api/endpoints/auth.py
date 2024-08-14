from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.db.session import get_db
from app.core.security import create_access_token
from app.services import auth_service
from app.api.crud import user as user_crud
from app.models.login import LoginRequest
from app.schemas.user import UserMinimal  # Import UserMinimal schema

from dotenv import load_dotenv
import getpass
import os

load_dotenv()

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

router = APIRouter()

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return user_crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(login_request: LoginRequest, db: Session = Depends(get_db)):

    user = auth_service.authenticate(db, email=login_request.username, password=login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = access_token = create_access_token(user_id=user.user_id, email=user.email)
    user_data = UserMinimal(
        username=user.username,
        email=user.email,
        user_id=user.user_id,
    )
    
    print("GEMINI KEY",GEMINI_API_KEY)
    
    return {"user": user_data, "access_token": access_token, "token_type": "bearer"}
