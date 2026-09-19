from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.predict import predict_machine_failure


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

        return result

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )