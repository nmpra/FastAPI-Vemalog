from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post(
    "",
    response_model=schemas.VehicleResponse,
    status_code=201,
)
def create_vehicle(vehicle: schemas.VehicleCreate, db: db_dependency):
    query = db.execute(
        select(models.User).where(models.User.id == vehicle.user_id)
    ).scalar_one_or_none()
    if not query:
        raise HTTPException(
            status_code=404,
            detail=f"User with ID {vehicle.user_id} could not be found.",
        )
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.get("/{vehicle_id}", response_model=schemas.VehicleResponse)
def get_vehicle(vehicle_id: int, db: db_dependency):
    db_vehicle = db.get(models.Vehicle, vehicle_id)
    if not db_vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found"
        )
    return db_vehicle


@router.get("/", response_model=list[schemas.VehicleResponse])
def get_all_vehicles(db: db_dependency):
    vehicles = db.execute(select(models.Vehicle)).scalars().all()
    return vehicles


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: db_dependency):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found"
        )
    db.delete(db_vehicle)
    db.commit()
    return {"messages": f"vehicle {db_vehicle.name} was succesfully deleted"}
