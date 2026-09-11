from fastapi import HTTPException


def vehicle_update_validator(vehicle, updates):
    if "current_mileage" in updates:
        if updates["current_mileage"] <= vehicle.current_mileage:
            raise HTTPException(
                status_code=400,
                detail="New mileage can not be less or same than current mileage",
            )

    if "last_oil_change" in updates:
        if updates["last_oil_change"] <= vehicle.current_mileage:
            raise HTTPException(
                status_code=400,
                detail="Last oil change mileage can not be less or same than current mileage",
            )

    if "last_maintenance" in updates:
        if updates["last_maintenance"] <= vehicle.current_mileage:
            raise HTTPException(
                status_code=400,
                detail="Last maintenance mileage can not be less or same than current mileage",
            )
