import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------
# MODEL PATH
# ---------------------------------------------------------

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "drushti_ai_model.joblib"
)
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "ai4i2020.csv"
FEATURE_COLUMNS = [
    "Type",
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]",
]
NUMERIC_FEATURES = FEATURE_COLUMNS[1:]
MEDIUM_RISK_THRESHOLD = 0.05
HIGH_RISK_THRESHOLD = 0.5

TRAINING_RANGES = {
    "Air temperature [K]": (295.3, 304.5),
    "Process temperature [K]": (305.7, 313.8),
    "Rotational speed [rpm]": (1168, 2886),
    "Torque [Nm]": (3.8, 76.6),
    "Tool wear [min]": (0, 253),
}
FAILURE_MODE_NAMES = {
    "TWF": "Tool wear",
    "HDF": "Heat dissipation",
    "PWF": "Power system",
    "OSF": "Overstrain",
    "RNF": "Unspecified failure",
}
MODEL_VALIDATION = {
    "dataset": "AI4I 2020",
    "test_examples": 2000,
    "test_failures": 68,
    "detected_failures": 49,
    "missed_failures": 19,
    "false_alarms": 9,
    "precision_percent": 84.5,
    "recall_percent": 72.1,
    "risk_bands": {
        "low": {"cases": 1843, "failures": 6, "observed_failure_percent": 0.3},
        "medium": {"cases": 99, "failures": 13, "observed_failure_percent": 13.1},
        "high": {"cases": 58, "failures": 49, "observed_failure_percent": 84.5},
    },
}


# Load trained model
model = joblib.load(MODEL_PATH)
_reference_data = pd.read_csv(DATA_PATH)
_reference_features = _reference_data[FEATURE_COLUMNS]
_reference_labels = _reference_data["Machine failure"]
_training_features, _ = train_test_split(
    _reference_features,
    test_size=0.2,
    random_state=42,
    stratify=_reference_labels,
)
_training_rows = _reference_data.loc[_training_features.index]
_failed_training_rows = _training_rows[
    _training_rows["Machine failure"] == 1
]
_range_scaler = StandardScaler().fit(_training_features[NUMERIC_FEATURES])


def _similarity_features(machine_rows):
    machine_types = pd.get_dummies(machine_rows["Type"])
    machine_types = machine_types.reindex(
        columns=["H", "L", "M"],
        fill_value=0,
    )
    numeric_values = _range_scaler.transform(machine_rows[NUMERIC_FEATURES])
    return np.column_stack((machine_types.to_numpy(), numeric_values))


_failure_neighbors = NearestNeighbors(
    n_neighbors=min(5, len(_failed_training_rows))
).fit(_similarity_features(_failed_training_rows))


def _find_possible_failure_modes(machine_rows):
    _, neighbor_indices = _failure_neighbors.kneighbors(
        _similarity_features(machine_rows)
    )
    nearby_failures = _failed_training_rows.iloc[neighbor_indices[0]]
    mode_counts = {
        mode: int(nearby_failures[mode].sum())
        for mode in FAILURE_MODE_NAMES
    }
    ranked_modes = sorted(
        mode_counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    return [
        {
            "code": mode,
            "name": FAILURE_MODE_NAMES[mode],
            "similar_examples": count,
            "examples_checked": len(nearby_failures),
        }
        for mode, count in ranked_modes[:3]
        if count > 0
    ]


def _classify_failure_risk(failure_probability):
    if failure_probability >= HIGH_RISK_THRESHOLD:
        return 1, "High Risk"
    if failure_probability >= MEDIUM_RISK_THRESHOLD:
        return 0, "Medium Risk"
    return 0, "Low Risk"


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

    out_of_range_features = [
        feature
        for feature, (minimum, maximum) in TRAINING_RANGES.items()
        if not minimum <= machine_data.at[0, feature] <= maximum
    ]
    possible_failure_modes = (
        _find_possible_failure_modes(machine_data)
        if not out_of_range_features
        else []
    )

    # Get failure probability
    failure_probability = model.predict_proba(
        machine_data
    )[0, 1]

    predicted_failure, risk_level = _classify_failure_risk(
        failure_probability
    )

    return {
        "failure_probability": float(
            failure_probability
        ),
        "predicted_failure": predicted_failure,
        "risk_level": risk_level,
        "input_supported": not out_of_range_features,
        "out_of_range_features": out_of_range_features,
        "possible_failure_modes": possible_failure_modes,
        "model_validation": MODEL_VALIDATION,
    }