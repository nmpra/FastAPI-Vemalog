from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
import models
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]

app = FastAPI()

@app.post("/users/", response_model=schemas.UserResponse, status_code=201, tags=["Users"])
def create_user(user: schemas.UserCreate, db: db_dependency):

    # Buat ngecek apakah ada user yang udah make nama itu, biar usernamenya unik
    query = db.execute(select(models.User).where(models.User.name == user.name))
    existing_user = query.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with that name already exist")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}",  response_model=schemas.UserResponse, tags=["Users"])
def get_user(user_id: int, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    user = query.scalars().first()
    if not user:
        raise HTTPException(status_code=400, detail=f"User with ID {user_id} could not be found")
    return user

@app.get("/users", response_model=list[schemas.UserResponse], tags=["Users"])
def get_all_user(db: db_dependency):
    users = db.execute(select(models.User)).scalars().all()
    return users

@app.get("/users/{user_id}/vehicles", response_model=list[schemas.VehicleResponse], tags=["Users"])
def get_user_vehicles(user_id: int, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = query.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} could not be found")
    query = db.execute(select(models.Vehicle).where(models.Vehicle.user_id == user_id))
    vehicles = query.scalars().all()
    return vehicles

@app.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = query.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} could not be found")
    db.delete(existing_user)
    db.commit()
    return {"messages": f"user {existing_user.name} was succesfully deleted"}

@app.post("/vehicles/", response_model=schemas.VehicleResponse, status_code=201, tags=["Vehicles"])
def create_vehicle(vehicle: schemas.VehicleCreate, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == vehicle.user_id)).scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail=f"User with ID {vehicle.user_id} could not be found.")
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.get("/vehicles/{vehicle_id}", response_model=schemas.VehicleResponse, tags=["Vehicles"])
def get_vehicle(vehicle_id: int, db: db_dependency):
    db_vehicle = db.get(models.Vehicle, vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found")
    return db_vehicle

@app.get("/vehicles/", response_model=list[schemas.VehicleResponse], tags=["Vehicles"])
def get_all_vehicles(db: db_dependency):
    vehicles = db.execute(select(models.Vehicle)).scalars().all()
    return vehicles

@app.delete("/vehicles/{vehicle_id}", tags=["Vehicles"])
def delete_vehicle(vehicle_id: int, db: db_dependency):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found")
    db.delete(db_vehicle)
    db.commit()
    return {"messages": f"vehicle {db_vehicle.name} was succesfully deleted"}

@app.patch("/vehicles/{vehicle_id}/mileage", response_model=schemas.UpdateResponse, tags=["Vehicle Detail"])
def update_vehicle_mileage(vehicle_id: int, new_mileage: schemas.MileageUpdate, db: db_dependency):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found")
    
    update_dict = new_mileage.model_dump(exclude_unset=True)

    if update_dict["current_mileage"] <= db_vehicle.current_mileage:
        raise HTTPException(status_code=400, detail="New mileage can not be less or same than current mileage")
    
    for field, value in update_dict.items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.patch("/vehicles/{vehicle_id}/oil_update", response_model=schemas.UpdateResponse, tags=["Vehicle Detail"])
def update_vehicle_oil(vehicle_id: int, db: db_dependency):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found")
    db_vehicle.last_oil_change = db_vehicle.current_mileage
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.patch("/vehicles/{vehicle_id}/maintenance_update", response_model=schemas.UpdateResponse, tags=["Vehicle Detail"])
def update_vehicle_maintenance(vehicle_id: int, db: db_dependency):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found")
    db_vehicle.last_maintenance = db_vehicle.current_mileage
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.patch("/vehicles/{vehicle_id}/update_vehicle", response_model=schemas.VehicleResponse, tags=["Vehicle Detail"])
def update_vehicle_data(vehicle_id: int, vehicle_data: schemas.VehicleUpdate, db: db_dependency):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found")
    
    update_dict = vehicle_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle    