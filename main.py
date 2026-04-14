from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/vehicles/", response_model=schemas.VehicleDetail)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@app.get("/vehicles/{vehicle_id}", response_model=schemas.VehicleDetail)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = db.query(models.Vehicle).get(vehicle_id)
    if not db_vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with id {vehicle_id} could not be found")
    return db_vehicle