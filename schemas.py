from pydantic import BaseModel, Field
from typing import Literal

class VehicleBase(BaseModel):
    name: str = Field(min_length=3)
    cc: int = Field(ge=50)
    license_plate: str
    vehicle_type: Literal["Car", "Motorcycle"]
    transmission: Literal["Manual", "Semi Auto", "Automatic"]

class VehicleCreate(VehicleBase):
    current_mileage: int = 0
    last_oil_change: int = 0
    last_maintenance: int = 0

class VehicleResponse(VehicleBase):
    id: int
    current_mileage: int
    last_oil_change: int
    last_maintenance: int
    
    oil_change_interval: int
    maintenance_interval: int
    remaining_oil: int
    remaining_maint: int

    class Config:
        from_attributes = True

class MileageUpdate(BaseModel):
    current_mileage: int = Field(ge=0, alias='new_mileage')

class UpdateResponse(VehicleBase):
    current_mileage: int
    last_oil_change: int = 0
    last_maintenance: int = 0
    remaining_oil: int
    remaining_maint: int

    class Config:
        from_attributes = True

class VehicleUpdate(BaseModel):
    name: str = Field(min_length=3)
    cc: int = Field(ge=50)
    license_plate: str
    vehicle_type: Literal["Car", "Motorcycle"]
    transmission: Literal["Manual", "Semi Auto", "Automatic"]