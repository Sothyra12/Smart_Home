from sqlalchemy.orm import Session
from app import models
from app.schemas.device import DeviceCreate

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()

def create_device(db: Session, device: DeviceCreate):
    db_device = models.Device(name=device.deviceName, image=device.image)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    # Add device to rooms
    if device.location:
        rooms = db.query(models.Room).filter(models.Room.id.in_(device.location)).all()
        for room in rooms:
            db_device.room_id = room.id
            break
        db.commit()

    return db_device