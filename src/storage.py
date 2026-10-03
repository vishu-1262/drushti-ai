import json
import os
import sqlite3
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


DATABASE_PATH = Path(
    os.getenv(
        "DRUSHTI_DATABASE_PATH",
        str(Path(__file__).resolve().parent.parent / "data" / "machine_records.sqlite3"),
    )
)


def _connect():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS machine_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT NOT NULL,
            recorded_at TEXT NOT NULL,
            machine_type TEXT NOT NULL,
            air_temperature REAL NOT NULL,
            process_temperature REAL NOT NULL,
            rotational_speed REAL NOT NULL,
            torque REAL NOT NULL,
            tool_wear REAL NOT NULL,
            failure_probability REAL NOT NULL,
            predicted_failure INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            input_supported INTEGER NOT NULL,
            out_of_range_features TEXT NOT NULL,
            possible_failure_modes TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_machine_readings_machine_time
            ON machine_readings(machine_id, recorded_at DESC);
        CREATE TABLE IF NOT EXISTS maintenance_schedules (
            machine_id TEXT PRIMARY KEY,
            last_serviced_on TEXT NOT NULL,
            interval_days INTEGER NOT NULL,
            updated_at TEXT NOT NULL
        );
        """
    )
    return connection


def _validate_machine_id(machine_id):
    machine_id = machine_id.strip()
    if not machine_id:
        raise ValueError("Machine ID cannot be empty.")
    if len(machine_id) > 80:
        raise ValueError("Machine ID must be 80 characters or fewer.")
    return machine_id


def save_prediction(machine_id, inputs, result):
    machine_id = _validate_machine_id(machine_id)
    recorded_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO machine_readings (
                machine_id, recorded_at, machine_type, air_temperature,
                process_temperature, rotational_speed, torque, tool_wear,
                failure_probability, predicted_failure, risk_level,
                input_supported, out_of_range_features,
                possible_failure_modes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                machine_id,
                recorded_at,
                inputs["machine_type"],
                inputs["air_temperature"],
                inputs["process_temperature"],
                inputs["rotational_speed"],
                inputs["torque"],
                inputs["tool_wear"],
                result["failure_probability"],
                result["predicted_failure"],
                result["risk_level"],
                int(result["input_supported"]),
                json.dumps(result["out_of_range_features"]),
                json.dumps(result["possible_failure_modes"]),
            ),
        )


def get_machine_history(machine_id, limit=10):
    machine_id = _validate_machine_id(machine_id)
    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT recorded_at, machine_type, air_temperature,
                   process_temperature, rotational_speed, torque, tool_wear,
                   failure_probability, predicted_failure, risk_level,
                   input_supported, out_of_range_features,
                   possible_failure_modes
            FROM machine_readings
            WHERE machine_id = ? COLLATE NOCASE
            ORDER BY recorded_at DESC, id DESC
            LIMIT ?
            """,
            (machine_id, limit),
        ).fetchall()

    history = []
    for row in rows:
        item = dict(row)
        item["input_supported"] = bool(item["input_supported"])
        item["out_of_range_features"] = json.loads(
            item["out_of_range_features"]
        )
        item["possible_failure_modes"] = json.loads(
            item["possible_failure_modes"]
        )
        history.append(item)
    return history


def save_maintenance_schedule(machine_id, last_serviced_on, interval_days):
    machine_id = _validate_machine_id(machine_id)
    if last_serviced_on > date.today():
        raise ValueError("Last service date cannot be in the future.")
    if interval_days < 1:
        raise ValueError("Maintenance interval must be at least one day.")

    updated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO maintenance_schedules (
                machine_id, last_serviced_on, interval_days, updated_at
            ) VALUES (?, ?, ?, ?)
            ON CONFLICT(machine_id) DO UPDATE SET
                last_serviced_on = excluded.last_serviced_on,
                interval_days = excluded.interval_days,
                updated_at = excluded.updated_at
            """,
            (
                machine_id,
                last_serviced_on.isoformat(),
                interval_days,
                updated_at,
            ),
        )
    return get_maintenance_schedule(machine_id)


def get_maintenance_schedule(machine_id):
    machine_id = _validate_machine_id(machine_id)
    with _connect() as connection:
        row = connection.execute(
            """
            SELECT last_serviced_on, interval_days, updated_at
            FROM maintenance_schedules
            WHERE machine_id = ? COLLATE NOCASE
            """,
            (machine_id,),
        ).fetchone()

    if row is None:
        return None

    last_serviced_on = date.fromisoformat(row["last_serviced_on"])
    due_date = last_serviced_on + timedelta(days=row["interval_days"])
    days_remaining = (due_date - date.today()).days
    status = "overdue" if days_remaining < 0 else (
        "due soon" if days_remaining <= 7 else "scheduled"
    )
    return {
        "machine_id": machine_id,
        "last_serviced_on": last_serviced_on.isoformat(),
        "interval_days": row["interval_days"],
        "due_date": due_date.isoformat(),
        "days_remaining": days_remaining,
        "status": status,
        "updated_at": row["updated_at"],
    }