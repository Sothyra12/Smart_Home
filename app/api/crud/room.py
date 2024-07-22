from sqlalchemy.orm import Session
from app.models import room as RoomModel
from app.models import device as Device
from app.schemas import room as schemas

def get_room(db: Session, room_id: int):
    return db.query(RoomModel).filter(RoomModel.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(RoomModel).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = RoomModel(name=room.roomName, image=room.image)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    # Add devices to the room
    if room.devices:
        devices = db.query(Device).filter(Device.id.in_(room.devices)).all()
        for device in devices:
            device.room_id = db_room.id
        db.commit()

    return db_room