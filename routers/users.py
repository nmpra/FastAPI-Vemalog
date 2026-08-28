from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.orm import Session

import models
from auth import (
    create_access_token,
    hash_password,
    oauth2_scheme,
    verify_access_token,
    verify_password,
)
from config import settings
from database import get_db
from schemas import (
    Token,
    UpdateResponse,
    UserCreate,
    UserResponse,
    VehicleResponse,
    VehicleUpdate,
)

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: db_dependency):

    # Buat ngecek apakah ada user yang udah make nama itu, biar usernamenya unik dan case insensitive make lower
    query = db.execute(
        select(models.User).where(func.lower(models.User.name) == user.name.lower())
    )
    existing_user = query.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with that name already exist")

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


@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: db_dependency,
) -> models.User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Ekstrak user_id dari token (payload 'sub')
    user_id = verify_access_token(token)
    if user_id is None:
        raise credentials_exception

    # Ambil user dari database berdasarkan ID
    query = db.execute(select(models.User).where(models.User.id == int(user_id)))
    user = query.scalars().first()

    if user is None:
        raise credentials_exception

    return user


# Type alias biar gampang dipake di endpoint mana pun
user_dependency = Annotated[models.User, Depends(get_current_user)]


# 2. Endpoint /me (profil user yang lagi login)
@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: user_dependency):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    user = query.scalars().first()
    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with ID {user_id} could not be found"
        )
    return user


@router.get("", response_model=list[UserResponse])
def get_all_user(db: db_dependency):
    users = db.execute(select(models.User)).scalars().all()
    return users


@router.get("/{user_id}/vehicles", response_model=list[VehicleResponse])
def get_user_vehicles(user_id: int, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = query.scalars().first()
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} could not be found"
        )
    return existing_user.vehicles


@router.delete("/{user_id}")
def delete_user(user_id: int, db: db_dependency):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    existing_user = query.scalars().first()
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} could not be found"
        )
    db.delete(existing_user)
    db.commit()
    return {"messages": f"user {existing_user.name} was succesfully deleted"}


@router.patch(
    "/{user_id}/vehicles/{vehicle_id}/",
    response_model=UpdateResponse,
)
def update_vehicle_data(
    user_id: int,
    vehicle_id: int,
    vehicle_update: VehicleUpdate,
    db: db_dependency,
):
    query = db.execute(select(models.User).where(models.User.id == user_id))
    user = query.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f"User with ID {user_id} could not be found"
        )

    query = db.execute(
        select(models.Vehicle).where(
            models.Vehicle.user_id == user_id, models.Vehicle.id == vehicle_id
        )
    )
    vehicle = query.scalars().first()
    if not vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle with ID {vehicle_id} could not be found"
        )

    update_dict = vehicle_update.model_dump(exclude_unset=True)

    if update_dict["current_mileage"] <= vehicle.current_mileage:
        raise HTTPException(
            status_code=400,
            detail="New mileage can not be less or same than current mileage",
        )

    elif update_dict["last_oil_change"] < vehicle.current_mileage:
        raise HTTPException(
            status_code=400,
            detail="Last oil change mileage can not be less than current mileage",
        )

    elif update_dict["last_maintenance"] < vehicle.current_mileage:
        raise HTTPException(
            status_code=400,
            detail="Last maintenance mileage can not be less than current mileage",
        )

    for field, value in update_dict.items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)
    return vehicle
