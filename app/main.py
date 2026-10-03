from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.predict import MODEL_VALIDATION, predict_machine_failure
from src.storage import (
    get_machine_history,
    get_maintenance_schedule,
    save_maintenance_schedule,
    save_prediction,
)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="DRUSHTI AI",
    description="Industrial Machine Failure Risk Prediction API",
    version="1.0.0"
)


# ---------------------------------------------------------
# INPUT SCHEMA
# ---------------------------------------------------------

class MachineInput(BaseModel):

    machine_id: str = Field(
        default="MACHINE-001",
        min_length=1,
        max_length=80,
        description="ID used to keep this machine's reading history",
    )

    machine_type: str = Field(
        ...,
        description="Machine type: L, M, or H"
    )

    air_temperature: float = Field(
        ...,
        gt=0,
        description="Air temperature in Kelvin"
    )

    process_temperature: float = Field(
        ...,
        gt=0,
        description="Process temperature in Kelvin"
    )

    rotational_speed: float = Field(
        ...,
        ge=0,
        description="Rotational speed in rpm"
    )

    torque: float = Field(
        ...,
        ge=0,
        description="Torque in Nm"
    )

    tool_wear: float = Field(
        ...,
        ge=0,
        description="Tool wear in minutes"
    )


class MaintenanceScheduleInput(BaseModel):

    last_serviced_on: date
    interval_days: int = Field(..., ge=1, le=3650)


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "DRUSHTI AI API is running",
        "version": "1.0.0"
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "model": "loaded"
    }


@app.get("/model-info")
def model_info():

    return MODEL_VALIDATION


@app.get("/machines/{machine_id}/history")
def machine_history(machine_id: str):

    try:
        return get_machine_history(machine_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/machines/{machine_id}/maintenance")
def maintenance_schedule(machine_id: str):

    try:
        schedule = get_maintenance_schedule(machine_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    return schedule or {"configured": False, "machine_id": machine_id}


@app.put("/machines/{machine_id}/maintenance")
def update_maintenance_schedule(
    machine_id: str,
    schedule: MaintenanceScheduleInput,
):

    try:
        return save_maintenance_schedule(
            machine_id,
            schedule.last_serviced_on,
            schedule.interval_days,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# ---------------------------------------------------------
# PREDICTION ENDPOINT
# ---------------------------------------------------------

@app.post("/predict")
def predict(data: MachineInput):

    # Validate machine type
    if data.machine_type not in ["L", "M", "H"]:
        raise HTTPException(
            status_code=400,
            detail="machine_type must be L, M, or H."
        )

    try:

        result = predict_machine_failure(
            machine_type=data.machine_type,
            air_temperature=data.air_temperature,
            process_temperature=data.process_temperature,
            rotational_speed=data.rotational_speed,
            torque=data.torque,
            tool_wear=data.tool_wear
        )

        save_prediction(
            data.machine_id,
            data.model_dump(exclude={"machine_id"}),
            result,
        )
        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )