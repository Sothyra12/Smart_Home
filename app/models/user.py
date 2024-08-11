from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
# from .device_consumption import DeviceConsumption

Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    image = Column(String(255))  # Add this line
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="rooms")
    devices = relationship("Device", back_populates="room")

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="scenes")
    scene_devices = relationship("SceneDevice", back_populates="scene")

class SceneDevice(Base):
    __tablename__ = "scene_devices"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    is_on = Column(Boolean)
    settings = Column(String(1024))

    scene = relationship("Scene", back_populates="scene_devices")
    device = relationship("Device", back_populates="scene_devices")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    type = Column(String(50))
    image = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True)
    is_on = Column(Boolean, nullable=True)
    power_rating = Column(Float, nullable=True)
    last_updated = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    brand = Column(String(50), nullable=True)
    model_number = Column(String(50), nullable=True)

    user = relationship("User", back_populates="devices")
    room = relationship("Room", back_populates="devices")
    scene_devices = relationship("SceneDevice", back_populates="device")
    consumptions = relationship("DeviceConsumption", back_populates="device", cascade="all, delete-orphan")

    orm_mode = True

class DeviceConsumption(Base):
    __tablename__ = "device_consumption"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    consumption = Column(Float, nullable=False)
    #timestamp = Column(DateTime, nullable=True)

    device = relationship("Device", back_populates="consumptions")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True)
    full_name = Column(String(255))
    birth_date = Column(DateTime)

    user = relationship("User", back_populates="profile")
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))

        
    rooms = relationship("Room", back_populates="user")
    devices = relationship("Device", back_populates="user")
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    scenes = relationship("Scene", back_populates="user")