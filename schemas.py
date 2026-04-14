from pydantic import BaseModel, Field
from typing import Literal

# --- SCHEMA 1: Buat input (Apa yang dikirim User) ---
class VehicleBase(BaseModel):
    name: str = Field(min_length=3)
    cc: int = Field(ge=50)
    license_plate: str
    vehicle_type: Literal["Car", "Motorcycle"]
    transmission: Literal["Manual", "Semi Auto", "Automatic"]

class VehicleCreate(VehicleBase):
    # Data awal pas baru beli/daftar
    current_mileage: int = 0
    last_oil_change: int = 0
    last_maintenance: int = 0

# --- SCHEMA 2: Buat output (Apa yang dikirim ke User) ---
class VehicleResponse(VehicleBase):
    id: int
    current_mileage: int
    last_oil_change: int
    last_maintenance: int
    
    # Ini manggil @property yang ada di models.py
    oil_change_interval: int
    maintenance_interval: int
    remaining_oil: int
    remaining_maint: int

    class Config:
        # WAJIB! Biar Pydantic bisa narik data dari @property SQLAlchemy
        from_attributes = True

# --- SCHEMA 3: Buat Update (Khusus buat nambah KM) ---
class MileageUpdate(BaseModel):
    current_mileage: int = Field(ge=0, alias='new_mileage')

class MileageResponse(VehicleBase):
    current_mileage: int
    remaining_oil: int
    remaining_maint: int

    class Config:
        from_attributes = True