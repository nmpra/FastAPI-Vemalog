from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import models
from auth import get_current_user
from database import get_db
from schemas import VehicleCreate, VehicleResponse

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[models.User, Depends(get_current_user)]


router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post(
    "",
    response_model=VehicleResponse,
    status_code=201,
)
def create_vehicle(
    vehicle: VehicleCreate, current_user: user_dependency, db: db_dependency
):
    db_vehicle = models.Vehicle(**vehicle.model_dump(), user_id=current_user.id)
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.delete("/{vehicle_id}")
def delete_vehicle(current_user: user_dependency, vehicle_id: int, db: db_dependency):
    query = db.execute(
        select(models.Vehicle).where(
            models.Vehicle.user_id == current_user.id, models.Vehicle.id == vehicle_id
        )
    )
    vehicle = query.scalars().first()
    if not vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found"
        )
    db.delete(vehicle)
    db.commit()
    return {
        "messages": f"vehicle {vehicle.brand} {vehicle.model} was succesfully deleted"
    }
