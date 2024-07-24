from sqlalchemy.orm import Session
from app import schemas
from app.models.user import Room
from app.models.user import Device

def get_room(db: Session, room_id: int):
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100, user_id: int =0):
    return db.query(Room).filter(Room.user_id == user_id).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate, user_id: int):
    db_room = Room(name=room.name, image=room.image, user_id=user_id)
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