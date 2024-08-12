from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas.device import DeviceCreate, DeviceConsumptionCreate
from datetime import datetime


from app.models.user import Device, DeviceConsumption

def get_device(db: Session, device_id: int):
    return db.query(Device).filter(Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100, user_id: int = 0):
    return db.query(Device).filter(Device.user_id == user_id).offset(skip).limit(limit).all()

def create_device(db: Session, device: DeviceCreate, user_id: int):
    db_device = Device(name=device.name, image=device.image,is_on=device.is_on, user_id=user_id, room_id=device.room_id, type=device.type, power_rating=device.power_rating, brand=device.brand, model_number=device.model_number)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)

    if hasattr(device, 'location') and device.location:
        rooms = db.query(models.Room).filter(models.Room.id.in_(device.location)).all()
        for room in rooms:
            db_device.room_id = room.id
            break
        db.commit()

    return db_device

def add_device_consumption(db: Session, device_id: int, start_time: datetime, end_time: datetime, power_consumption: float = 0.0):        
    device_consumption = DeviceConsumption(device_id=device_id, start_time=start_time, end_time=end_time, consumption=power_consumption)
    db.add(device_consumption)
    db.commit()
    db.refresh(device_consumption)
    return device_consumption