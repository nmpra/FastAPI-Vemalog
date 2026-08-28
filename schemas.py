from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: str = Field(min_length=3)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class VehicleBase(BaseModel):
    brand: str = Field(min_length=3)
    model: str = Field(min_length=3)
    cc: int = Field(ge=50)
    license_plate: str
    vehicle_type: Literal["Car", "Motorcycle"]
    transmission: Literal["Manual", "Semi Auto", "Automatic"]


class VehicleCreate(VehicleBase):
    user_id: int
    current_mileage: int = 0
    last_oil_change: int = 0
    last_maintenance: int = 0


class VehicleResponse(VehicleBase):
    id: int
    user: UserResponse
    current_mileage: int
    last_oil_change: int
    last_maintenance: int

    oil_change_interval: int
    maintenance_interval: int
    remaining_oil: int
    remaining_maint: int

    model_config = ConfigDict(from_attributes=True)


class UpdateResponse(VehicleBase):
    current_mileage: int
    last_oil_change: int = 0
    last_maintenance: int = 0
    remaining_oil: int
    remaining_maint: int

    model_config = ConfigDict(from_attributes=True)


class VehicleUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=3)
    model: str | None = Field(default=None, min_length=3)
    cc: int | None = Field(default=None, ge=50)
    license_plate: str | None = None
    vehicle_type: Literal["Car", "Motorcycle"] | None = None
    transmission: Literal["Manual", "Semi Auto", "Automatic"] | None = None
    current_mileage: int | None = None
    last_oil_change: int | None = None
    last_maintenance: int | None = None
