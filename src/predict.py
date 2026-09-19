import joblib
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# MODEL PATH
# ---------------------------------------------------------

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "drushti_ai_model.joblib"
)


# Load trained model
model = joblib.load(MODEL_PATH)


# ---------------------------------------------------------
# PREDICTION FUNCTION
# ---------------------------------------------------------

def predict_machine_failure(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear
):

    # Validate machine type
    if machine_type not in ["L", "M", "H"]:
        raise ValueError("Type must be L, M, or H.")

    # Validate numerical inputs
    if air_temperature <= 0:
        raise ValueError(
            "Air temperature must be greater than 0 K."
        )

    if process_temperature <= 0:
        raise ValueError(
            "Process temperature must be greater than 0 K."
        )

    if rotational_speed < 0:
        raise ValueError(
            "Rotational speed cannot be negative."
        )

    if torque < 0:
        raise ValueError(
            "Torque cannot be negative."
        )

    if tool_wear < 0:
        raise ValueError(
            "Tool wear cannot be negative."
        )

    # Create input DataFrame
    machine_data = pd.DataFrame([{
        "Type": machine_type,
        "Air temperature [K]": air_temperature,
        "Process temperature [K]": process_temperature,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear
    }])

    # Get failure probability
    failure_probability = model.predict_proba(
        machine_data
    )[0, 1]

    # Convert probability into prediction
    predicted_failure = int(
        failure_probability >= 0.5
    )

    # Determine risk
    if predicted_failure == 1:
        risk_level = "High Risk"
    else:
        risk_level = "Low Risk"

    return {
        "failure_probability": float(
            failure_probability
        ),
        "predicted_failure": predicted_failure,
        "risk_level": risk_level
    }