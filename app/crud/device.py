from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas.device import DeviceCreate, DeviceConsumptionCreate, DeviceWithConsumption
from datetime import datetime
from app.models.user import Device, DeviceConsumption, Room
from typing import List


# AI Related

from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

import getpass
import os
from dotenv import load_dotenv

load_dotenv()

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


def get_user_devices_and_consumption(db: Session, user_id: int) -> List[DeviceWithConsumption]:
    rooms = db.query(Room).filter(Room.user_id == user_id).all()
    data = []

    for room in rooms:
        devices = db.query(Device).filter(Device.room_id == room.id).all()
        for device in devices:
            consumption = db.query(DeviceConsumption)\
                            .filter(DeviceConsumption.device_id == device.id)\
                            .order_by(DeviceConsumption.timestamp.desc())\
                            .first()
            
            data.append(DeviceWithConsumption(
                id=device.id,
                name=device.name,  # Ensure this is populated correctly
                type=device.type,
                image=device.image,
                is_on=device.is_on,
                power_rating=device.power_rating,
                room_id=device.room_id,
                user_id=device.user_id,
                brand=device.brand,
                model_number=device.model_number,
                energy_limit=device.energy_limit,
                latest_consumption=consumption.consumption if consumption else None,
                timestamp=consumption.timestamp if consumption else None
            ))

    return data


def get_devices_by_room(db: Session, room_id: int):
    return db.query(Device).filter(Device.room_id == room_id).all()

def generate_response_with_rag(db: Session, user_id: int, user_query: str):
    
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

    # Step 1: Retrieve context
    device_data = get_user_devices_and_consumption(db, user_id)
    context = ""
    
    for entry in device_data:
        context += (
            f"Room ID: {entry.room_id}, Device: {entry.name}, "
            f"Brand: {entry.brand}, Model Number: {entry.model_number}, "
            f"Latest Consumption: {entry.latest_consumption} kWh at {entry.timestamp}.\n"
        )
    
    # Step 2: Prepare the AI model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    
    # Step 3: Create the prompt for AI
    PROMPT_TEMPLATE = """
    Use the following context to answer the user's query:
    
    {context}
    
    User Query: {user_query}
    
    AI Response:
    """
    
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, user_query=user_query)
    
    # Step 4: Generate response using the AI model
    ai_msg = llm.invoke(prompt)
    
    # Step 5: Parse and format the response
    response_text = ai_msg.content.strip()
    
    formatted_response = {
        "response": response_text
    }
    
    return response_text

