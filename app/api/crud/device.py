from sqlalchemy.orm import Session
from app.models.device import Device
from app.models.room import Room
from app import schemas

def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Device).offset(skip).limit(limit).all()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = Device(name=device.deviceName, image=device.image)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    # Add device to rooms
    if device.location:
        rooms = db.query(Room).filter(Room.id.in_(device.location)).all()
        for room in rooms:
            db_device.room_id = room.id
            break 
        db.commit()

    return db_device