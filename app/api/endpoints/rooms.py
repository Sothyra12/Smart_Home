from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import room as crud
from app.schemas import room as schemas
from app.db.session import get_db
from app.core.utils import get_current_user
from app.core.security import TokenData

router = APIRouter()

@router.post("/", response_model=schemas.Room)
def create_room(
    room: schemas.RoomCreate, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
):
    user_id = current_user.user_id
    return crud.create_room(db=db, room=room, user_id=user_id)

@router.get("/", response_model=List[schemas.Room])
def read_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)):
    rooms = crud.get_rooms(db, skip=skip, limit=limit, user_id=current_user.user_id)
    return rooms

@router.get("/{room_id}", response_model=schemas.Room)
def read_room(room_id: int, db: Session = Depends(get_db)):
    db_room = crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room
