from fastapi import FastAPI, HTTPException, Form
from typing import Annotated
from schemas import VehicleCreate
from services import GarageServices
from models import Car, Motorcycle

app = FastAPI()
my_garage = GarageServices()

def dummy_data(garage):
    m1 = Motorcycle(
        id= 1,
        name="Vario 160 eSP+", 
        cc=160, 
        license_plate="H 1234 ABC", 
        transmission="Automatic"
    )
    
    m2 = Motorcycle(
        id= 2,
        name="ZX-25RR", 
        cc=250, 
        license_plate="B 3344 SSS", 
        transmission="Manual"
    )

    c1 = Car(
        id= 3,
        name="Innova Venturer", 
        cc=2400, 
        license_plate="AD 1 ABC", 
        transmission="Automatic"
    )

    garage.add_vehicle(m1)
    garage.add_vehicle(m2)
    garage.add_vehicle(c1)

dummy_data(my_garage)

@app.get("/vehicles", tags=["Garage"])
def get_all_vehicles():
    vehicles = [v.__dict__ for v in my_garage.get_all_veh()]
    return {"vehicles": vehicles}

@app.get("/vehicles/{id}", tags=["Garage"])
def get_vehicle(id: int):
    vehicle = my_garage.find_vehicle(id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {id} could not be found.")
    return {"vehicle": vehicle}


@app.post("/vehicles", tags=["Garage"])
def add_new_vehicles(payload: VehicleCreate):
    if payload.vehicle_type == "Motorcycle":
        obj_veh = Motorcycle(id=None, name=payload.name, cc=payload.cc, license_plate=payload.license_plate, transmission=payload.transmission)
    if payload.vehicle_type == "Car":
        obj_veh = Car(id=None, name=payload.name, cc=payload.cc, license_plate=payload.license_plate, transmission=payload.transmission)
    else:
        raise HTTPException(status_code=400, detail=f"Vehicle type {payload.vehicle_type} is not registered.")
    new_vehicle = my_garage.add_vehicle(obj_veh)
    return {"messages": f"{new_vehicle.name} added succesfully",
            "id": new_vehicle.id,
            "detail": new_vehicle.get_info()}

@app.delete("/vehicles/{id}", tags=["Garage"])
def delete_vehicle(id: int):
    try:
        my_garage.remove_vehicle(id)
        return {"message": f"Vehicle with ID {id} succesfully removed.",
                "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.patch("/vehicles/{id}/update_mileage", tags=["Vehicle Management"])
def update_vehicle_mileage(id: int, new_mileage: Annotated[int, Form()]):
    vehicle = my_garage.find_vehicle(id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {id} could not be found.")
    try:
        new_mil = vehicle.mileage_update(new_mileage)
        if new_mil:
            return {"message": "Succesfully updated vehicle mileage",
                    "mileage": f"{vehicle._prev_mileage} => {vehicle._mileage}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/vehicles/{id}/update_oil", tags=["Vehicle Management"])
def update_oil_mileage(id: int):
    vehicle = my_garage.find_vehicle(id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {id} could not be found.")
    vehicle.oil_update()
    return {"message": "Succesfully updated vehicle oil mileage",
            "mileage": f"{vehicle._last_oil_mileage}"}

@app.get("/vehicles/{id}/oil_status", tags=["Vehicle Management"])
def vehicle_oil_status(id: int):
    vehicle = my_garage.find_vehicle(id)
    if vehicle is None:
        raise HTTPException(status_code=404, detail=f"Vehicle with ID {id} could not be found.")
    con, status = vehicle.oil_status()
    if con:
        return {"oil status": "Good",
                "remaining mileage": f"{status}km"}
    else:
        return {"oil status": "Bad",
                "message": "This vehicle need new engine oil"}