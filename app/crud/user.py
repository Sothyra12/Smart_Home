from sqlalchemy.orm import Session
from app.models.user import User, UserProfile
from app.schemas.user import CombinedUserProfileUpdate
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.schemas.user import UserUpdate

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_profile_by_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()


def update_user(db: Session, db_obj: User, obj_in: UserUpdate) -> User:
    update_data = obj_in.dict(exclude_unset=True)
    if 'password' in update_data:
        hashed_password = get_password_hash(update_data['password'])
        del update_data['password']
        update_data['password_hash'] = hashed_password
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_user_and_profile(db: Session, user: User, user_profile: UserProfile, obj_in: CombinedUserProfileUpdate) -> User:
    # Update user table
    user_update_data = obj_in.dict(exclude={'full_name', 'birth_date'}, exclude_unset=True)
    if 'password' in user_update_data:
        hashed_password = get_password_hash(user_update_data['password'])
        del user_update_data['password']
        user_update_data['password_hash'] = hashed_password
    for field, value in user_update_data.items():
        setattr(user, field, value)

    # Update user_profile table
    profile_update_data = obj_in.dict(include={'full_name', 'birth_date'}, exclude_unset=True)
    for field, value in profile_update_data.items():
        if value is not None:  # Only update fields that are provided
            setattr(user_profile, field, value)

    db.add(user)
    db.add(user_profile)
    db.commit()
    db.refresh(user)
    db.refresh(user_profile)
    return user
