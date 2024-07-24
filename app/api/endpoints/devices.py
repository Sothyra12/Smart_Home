from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud import device as crud
from app.schemas.device import Device as DeviceSchema, DeviceCreate as DeviceCreateSchema
from app.db.session import get_db
from app.core.utils import get_current_user
from app.core.security import TokenData

router = APIRouter()

@router.post("/", response_model=DeviceSchema)
def create_device(
    device: DeviceCreateSchema, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)):
    return crud.create_device(db=db, device=device, user_id=current_user.user_id)

@router.get("/", response_model=List[DeviceSchema])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)):
    devices = crud.get_devices(db, skip=skip, limit=limit, user_id=current_user.user_id)
    for device in devices:
        if device.type is None:
            device.type = ""
    return devices

@router.get("/{device_id}", response_model=DeviceSchema)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device