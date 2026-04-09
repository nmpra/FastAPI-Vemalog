from pydantic import BaseModel, Field
from typing import Literal

class VehicleCreate(BaseModel):
    name: str = Field(min_length=3)
    cc: int = Field(min_length=2)
    license_plate: str = Field(min_length=3)
    vehicle_type: str | Literal["Car", "Motorcycle"]
    transmission: str | Literal["Manual", "Semi Auto", "Automatic"]