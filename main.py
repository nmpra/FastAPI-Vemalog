from fastapi import FastAPI, HTTPException, Form
from typing import Annotated
from schema import VehicleCreate
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

@app.get("/vehicles")
def get_all_vehicles():
    vehicles = [v.__dict__ for v in my_garage.get_all_veh()]
    return {"vehicles": vehicles}

@app.post("/vehicles")
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