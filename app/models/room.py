from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="rooms")
    devices = relationship("Device", back_populates="room")