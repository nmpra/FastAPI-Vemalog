from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/vehicles/", response_model=schemas.VehicleResponse, tags=["Vehicles"])
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.get("/vehicles/{vehicle_id}", response_model=schemas.VehicleResponse, tags=["Vehicles"])
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} could not be found")
    return db_vehicle

@app.delete("/vehicles/{vehicle_id}", tags=["Vehicles"])
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} could not be found")
    db.delete(db_vehicle)
    db.commit()
    return {"messages": f"vehicle {db_vehicle.name} was succesfully deleted"}

@app.patch("/vehicles/{vehicle_id}/mileage", response_model=schemas.UpdateResponse, tags=["Vehicle Detail"])
def update_vehicle_mileage(vehicle_id: int, new_mileage: schemas.MileageUpdate, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} could not be found")
    
    update_dict = new_mileage.model_dump(exclude_unset=True)

    if update_dict["current_mileage"] <= db_vehicle.current_mileage:
        raise HTTPException(status_code=400, detail="New mileage can not be less or same than current mileage")
    
    for field, value in update_dict.items():
        setattr(db_vehicle, field, value)

    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.patch("/vehicles/{vehicle_id}/oil_update", response_model=schemas.UpdateResponse, tags=["Vehicle Detail"])
def update_vehicle_oil(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} could not be found")
    db_vehicle.last_oil_change = db_vehicle.current_mileage
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.patch("/vehicles/{vehicle_id}/maintenance_update", response_model=schemas.UpdateResponse, tags=["Vehicle Detail"])
def update_vehicle_maintenance(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} could not be found")
    db_vehicle.last_maintenance = db_vehicle.current_mileage
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle