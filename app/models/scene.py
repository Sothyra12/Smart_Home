from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="scenes")
    scene_devices = relationship("SceneDevice", back_populates="scene")

class SceneDevice(Base):
    __tablename__ = "scene_devices"

    id = Column(Integer, primary_key=True, index=True)
    scene_id = Column(Integer, ForeignKey("scenes.id"))
    device_id = Column(Integer, ForeignKey("devices.id"))
    is_on = Column(Boolean)
    settings = Column(String(1024))  # You might want to use JSON type here depending on your database

    scene = relationship("Scene", back_populates="scene_devices")
    device = relationship("Device", back_populates="scene_devices")