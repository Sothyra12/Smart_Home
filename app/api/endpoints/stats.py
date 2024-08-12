from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.crud import device as crud
from app.schemas.device import Device as DeviceSchema, DeviceCreate as DeviceCreateSchema, DeviceConsumption as DeviceConsumptionSchema, DeviceConsumptionCreate
from app.db.session import get_db
from app.core.utils import get_current_user
from app.core.security import TokenData
from app.models.user import Device, DeviceConsumption
from app.schemas.user import EnergyUsage
from datetime import datetime, timedelta
from sqlalchemy import func

import random

router = APIRouter()


@router.get("/energy-usage", response_model=List[EnergyUsage])
async def get_energy_usage(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    # Fetch user's devices
    devices = crud.get_devices(db, skip=skip, limit=limit, user_id=current_user.user_id)
    
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found for this user")
    
    # Get device IDs
    device_ids = [device.id for device in devices]
    
    # Fetch energy usage data from DeviceConsumption table
    energy_usage_data = (
        db.query(DeviceConsumption)
        .filter(DeviceConsumption.device_id.in_(device_ids))
        .order_by(DeviceConsumption.start_time.desc())
        .limit(limit)
        .offset(skip)
        .all()
    )
    
    if not energy_usage_data:
        raise HTTPException(status_code=404, detail="No energy usage data found for user's devices")
    
    # Convert DeviceConsumption objects to EnergyUsage schema
    return [
        EnergyUsage(
            id=usage.id,
            device_id=usage.device_id,
            start_time=usage.start_time,
            end_time=usage.end_time,
            consumption=usage.consumption,
            timestamp=usage.timestamp
        )
        for usage in energy_usage_data
    ]

@router.get("/energy-usage/summary")
async def get_energy_usage_summary(
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user)
):
    # Fetch user's devices
    devices = crud.get_devices(db, user_id=current_user.user_id)
    
    if not devices:
        raise HTTPException(status_code=404, detail="No devices found for this user")
    
    device_ids = [device.id for device in devices]
    
    # Calculate summary statistics
    current_time = datetime.utcnow()
    daily_start = current_time - timedelta(days=1)
    monthly_start = current_time - timedelta(days=30)
    
    current_usage = (
        db.query(func.sum(DeviceConsumption.consumption))
        .filter(DeviceConsumption.device_id.in_(device_ids))
        .filter(DeviceConsumption.end_time > current_time - timedelta(minutes=5))
        .scalar() or 0
    )
    
    daily_usage = (
        db.query(func.sum(DeviceConsumption.consumption))
        .filter(DeviceConsumption.device_id.in_(device_ids))
        .filter(DeviceConsumption.start_time > daily_start)
        .scalar() or 0
    )
    
    monthly_cost = (
        db.query(func.sum(DeviceConsumption.consumption * 0.15))  # Assuming $0.15 per kWh
        .filter(DeviceConsumption.device_id.in_(device_ids))
        .filter(DeviceConsumption.start_time > monthly_start)
        .scalar() or 0
    )
    
    return {
        "current_usage": round(current_usage, 2),
        "daily_usage": round(daily_usage, 2),
        "monthly_cost": round(monthly_cost, 2)
    }