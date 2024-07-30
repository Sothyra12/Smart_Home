from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import csv
from datetime import datetime

from app.crud import device as crud
from app.schemas.device import Device as DeviceSchema, DeviceCreate as DeviceCreateSchema
from app.db.session import get_db
from app.core.utils import get_current_user
from app.core.security import TokenData
from app.models.user import Device, DeviceConsumption

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


def get_power_consumption(device_type: str) -> float:
    with open('device_power_consumption.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['device_type'].lower() == device_type.lower():
                return float(row['power_consumption'])
    return 0.0  # Return 0 if device type not found

def record_device_usage(db: Session, device_id: int, duration: float):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise ValueError("Device not found")

    power_consumption = get_power_consumption(device.type)
    total_consumption = power_consumption * duration

    consumption = DeviceConsumption(
        device_id=device_id,
        timestamp=datetime.utcnow(),
        power_consumption=power_consumption,
        duration=duration,
        total_consumption=total_consumption
    )
    db.add(consumption)
    db.commit()
    return consumption


@router.get("/{room_id}/devices", response_model=List[DeviceSchema])
def read_room_devices(
    room_id: int, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    db_room = crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    if db_room.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this room")
    devices = crud.get_room_devices(db, room_id=room_id)
    return devices