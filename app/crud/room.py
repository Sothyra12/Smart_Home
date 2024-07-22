from sqlalchemy.orm import Session
from app import models, schemas

def get_room(db: Session, room_id: int):
    return db.query(models.Room).filter(models.Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Room).offset(skip).limit(limit).all()

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.roomName, image=room.image)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)

    # Add devices to the room
    if room.devices:
        devices = db.query(models.Device).filter(models.Device.id.in_(room.devices)).all()
        for device in devices:
            device.room_id = db_room.id
        db.commit()

    return db_room