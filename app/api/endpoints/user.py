from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import user as user_crud
from app.schemas.user import User, UserCreate, UserResponse, UserUpdate, CombinedUserProfileResponse, CombinedUserProfileUpdate, UserSettings, UserSettingsCreate
from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.core.utils import get_current_user
from app.models import user as user_model
from app.core.security import TokenData
from typing import List


router = APIRouter()

ALLOWED_USER_TYPES = ['Tech Enthusiast', 'Remote Manager', 'Eco-Conscious User', 'Family Oriented']

@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
def get_current_user_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(current_user)
    """
    Get current user's profile and user details.
    """
    return user_crud.get_user_profile_by_user_id(db, user_id=current_user.user_id)

@router.put("/me", response_model=CombinedUserProfileResponse)
def update_user_profile(
    user_update: CombinedUserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile and user details.
    """
    uid = int(current_user.user_id)
    cu = user_crud.get_user_profile_by_user_id(db, user_id=uid)

    if user_update.user_type:
        if user_update.user_type not in ALLOWED_USER_TYPES:
            raise HTTPException(status_code=400, detail="Invalid user type")
        if cu.user_type == "Administrator" and user_update.user_type != "Administrator":
            raise HTTPException(status_code=400, detail="Administrators cannot change their user type")
        if cu.user_type != "Administrator" and user_update.user_type == "Administrator":
            raise HTTPException(status_code=403, detail="Not enough permissions")
    
    user_profile = db.query(user_model.UserProfile).filter(user_model.UserProfile.user_id == current_user.user_id).first()
    if not user_profile:
        # Option 1: Create a new user profile
        user_profile = user_model.UserProfile(user_id=current_user.user_id)
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
    
    updated_user = user_crud.update_user_and_profile(db, user=cu, user_profile=user_profile, obj_in=user_update)
    return updated_user

@router.put("/{user_id}", response_model=CombinedUserProfileResponse)
def update_user_profile_by_id(
    user_id: int,
    user_update: CombinedUserProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a user's profile and user details by ID. Only for administrators.
    """
    if current_user.user_type != "Administrator":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_profile = db.query(user_model.UserProfile).filter(user_model.UserProfile.user_id == user.id).first()
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    if user_update.user_type:
        if user_update.user_type not in ALLOWED_USER_TYPES + ["Administrator"]:
            raise HTTPException(status_code=400, detail="Invalid user type")
    
    updated_user = user_crud.update_user_and_profile(db, db_obj=user, user_profile=user_profile, obj_in=user_update)
    return updated_user


@router.post("/settings/leave-home-office", response_model=UserSettings)
def save_leave_home_office_settings(
    settings: UserSettingsCreate, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
):
    user_id = current_user.user_id
    
    # Check if the setting already exists for the user
    existing_setting = db.query(user_model.UserSettings).filter_by(
        user_id=user_id, 
        setting_key=settings.setting_key
    ).first()

    if existing_setting:
        # Update the existing setting
        existing_setting.setting_value = settings.setting_value
        db.commit()
        db.refresh(existing_setting)
        return existing_setting
    else:
        # Create a new setting if it doesn't exist
        new_setting = user_model.UserSettings(
            user_id=user_id,
            setting_key=settings.setting_key,
            setting_value=settings.setting_value
        )
        db.add(new_setting)
        db.commit()
        db.refresh(new_setting)
        return new_setting

@router.get("/settings", response_model=List[UserSettings])
def get_all_user_settings(
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
):
    user_id = int(current_user.user_id)
    settings = db.query(user_model.UserSettings).filter(user_model.UserSettings.user_id == user_id).all()
    
    if not settings:
        raise HTTPException(status_code=404, detail="No settings found for this user")
    
    return settings