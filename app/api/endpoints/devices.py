from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import csv
from datetime import datetime

from app.crud import device as crud
from app.schemas.device import Device as DeviceSchema, DeviceCreate as DeviceCreateSchema, DeviceConsumption as DeviceConsumptionSchema, DeviceConsumptionCreate
from app.db.session import get_db
from app.core.utils import get_current_user
from app.core.security import TokenData
from app.models.user import Device, DeviceConsumption
from app.utils.csv_helpers import load_csv_data, get_unique_brands
from app.utils.file_selector import select_csv_file, device_mapping

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_DIR = os.path.join(BASE_DIR, "csv")

router = APIRouter()

@router.post("/", response_model=DeviceSchema)
def create_device(
    device: DeviceCreateSchema, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)):
    return crud.create_device(db=db, device=device, user_id=current_user.user_id)

@router.get("/", response_model=List[DeviceSchema])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)):
    devices = crud.get_devices(db, skip=skip, limit=limit, user_id=current_user.user_id)
    for device in devices:
        if device.type is None:
            device.type = ""
    return devices

@router.get("/{device_id}", response_model=DeviceSchema)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.post("/consumptions", response_model=DeviceConsumptionSchema)
def record_device_usage(consumption_data: DeviceConsumptionCreate, db: Session = Depends(get_db)):
    # Retrieve the device from the database
    device = db.query(Device).filter(Device.id == consumption_data.device_id).first()
    
    if not device:
        raise ValueError("Device not found")

    # Get the mapping entry based on the device type
    mapping_entry = device_mapping.get(device.type)
    if not mapping_entry:
        raise ValueError(f"No mapping found for device type: {device.type}")

    # Load the CSV file for the device type
    csv_file_path = select_csv_file(device.type)
    csv_data = load_csv_data(csv_file_path)
    field_mapping = mapping_entry["field_mapping"]

    # Find the row corresponding to the device's model number
    power_consumption = None
    for row in csv_data:
        if row[field_mapping["MODEL_NUM"]] == device.model_number:
            power_consumption = float(row[field_mapping["AEC"]])
            break
    
    if power_consumption is None:
        raise ValueError("Model number not found in CSV")

    # Calculate consumption
    hourly_consumption_rate = power_consumption / (365 * 24)
    total_consumption = hourly_consumption_rate * (consumption_data.end_time - consumption_data.start_time).total_seconds() / 3600

    # Record consumption in the database
    consumption = crud.add_device_consumption(
        db,
        device_id=consumption_data.device_id,
        start_time=consumption_data.start_time,
        end_time=consumption_data.end_time,
        power_consumption=total_consumption
    )


    return consumption


def get_power_consumption(device_type: str) -> float:

    csv_path = os.path.join(CSV_DIR, "002_clothes-washer-dryers.csv")
    #with open('/../../../csv/002_clothes-washer-dryers.csv', 'r') as f:
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            print(row)
            if row['device_type'].lower() == device_type.lower():
                return float(row['power_consumption'])
    return 0.0  # Return 0 if device type not found

@router.get("/{room_id}/devices", response_model=List[DeviceSchema])
def read_room_devices(
    room_id: int, 
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    db_room = crud.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    if db_room.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this room")
    devices = crud.get_room_devices(db, room_id=room_id)
    return devices


@router.get("/models/{device_type}/{brand_name}", response_model=List[str])
def get_models_by_device_and_brand(device_type: str, brand_name: str):
    try:
        # Get the correct CSV file path based on the device type
        csv_file_path = select_csv_file(device_type)
        
        # Load the CSV data
        csv_data = load_csv_data(csv_file_path)
        
        # Filter the models by brand name
        models = [row["MODEL_NUM_1"] for row in csv_data if row["BRAND_NAME"].lower() == brand_name.lower()]
        
        if not models:
            raise HTTPException(status_code=404, detail="No models found for the selected brand.")
        
        return models
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.get("/brands/{device_type}", response_model=List[str])
def get_brands_by_device_type(device_type: str):
    try:
        # Get the correct CSV file path based on the device type
        csv_file_path = select_csv_file(device_type)
        
        # Load the CSV data
        csv_data = load_csv_data(csv_file_path)
        
        # Get the unique brand names
        brands = get_unique_brands(csv_data)
        
        if not brands:
            raise HTTPException(status_code=404, detail="No brands found.")
        
        return brands
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))