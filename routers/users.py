from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
from auth import create_access_token, get_current_user, hash_password, verify_password
from config import settings
from database import get_db
from helper import vehicle_update_validator
from schemas import (
    Token,
    UpdateResponse,
    UserCreate,
    UserResponse,
    VehicleResponse,
    VehicleUpdate,
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[models.User, Depends(get_current_user)]


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: db_dependency):

    # Buat ngecek apakah ada user yang udah make nama itu, biar usernamenya unik dan case insensitive make lower
    query = db.execute(
        select(models.User).where(func.lower(models.User.name) == user.name.lower())
    )
    existing_user = query.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=400, detail="User with that name already exists"
        )

    new_user = models.User(name=user.name, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    # 1. Cari user berdasarkan name
    query = db.execute(
        select(models.User).where(
            func.lower(models.User.name) == form_data.username.lower()
        )
    )
    user = query.scalars().first()

    # 2. Validasi keberadaan user dan kecocokan password
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Generate JWT access token dengan payload ID user
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    # 4. Return token sesuai schema standar OAuth2
    return {"access_token": access_token, "token_type": "bearer"}


# 2. Endpoint /me (profil user yang lagi login)
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: user_dependency):
    return current_user


@router.get("/me/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_user_vehicle(vehicle_id: int, current_user: user_dependency, db: db_dependency):
    query = db.execute(
        select(models.Vehicle).where(
            models.Vehicle.user_id == current_user.id, models.Vehicle.id == vehicle_id
        )
    )
    vehicle = query.scalars().first()
    if not vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found"
        )
    return vehicle


@router.get("/me/vehicles", response_model=list[VehicleResponse])
def get_user_vehicles(current_user: user_dependency, db: db_dependency):
    return current_user.vehicles


@router.delete("/me")
def delete_user(current_user: user_dependency, db: db_dependency):
    db.delete(current_user)
    db.commit()
    return {"message": f"user {current_user.name} was successfully deleted"}


@router.patch(
    "/me/vehicles/{vehicle_id}/",
    response_model=UpdateResponse,
)
def update_vehicle_data(
    current_user: user_dependency,
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    db: db_dependency,
):
    query = db.execute(
        select(models.Vehicle).where(
            models.Vehicle.user_id == current_user.id, models.Vehicle.id == vehicle_id
        )
    )
    vehicle = query.scalars().first()
    if not vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found"
        )

    update_dict = vehicle_update.model_dump(exclude_unset=True)

    vehicle_update_validator(vehicle, update_dict)

    for field, value in update_dict.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)
    return vehicle
