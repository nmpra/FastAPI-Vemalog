from pydantic import BaseModel
from typing import Literal

class VehicleCreate(BaseModel):
    name: str
    cc: int
    license_plate: str
    vehicle_type: str | Literal["Car", "Motorcycle"]
    transmission: str | Literal["Manual", "Semi Auto", "Automatic"]