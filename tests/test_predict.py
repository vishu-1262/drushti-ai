from src.predict import predict_machine_failure


def test_valid_prediction():

    result = predict_machine_failure(
        machine_type="L",
        air_temperature=300,
        process_temperature=310,
        rotational_speed=1500,
        torque=50,
        tool_wear=100
    )

    assert "failure_probability" in result
    assert "predicted_failure" in result
    assert "risk_level" in result
    assert result["input_supported"] is True
    assert result["out_of_range_features"] == []
    assert result["possible_failure_modes"]
    assert result["model_validation"]["test_examples"] == 2000

    assert 0 <= result["failure_probability"] <= 1
    assert result["predicted_failure"] in [0, 1]
    assert result["risk_level"] in ["Low Risk", "High Risk"]


def test_invalid_machine_type():

    try:

        predict_machine_failure(
            machine_type="X",
            air_temperature=300,
            process_temperature=310,
            rotational_speed=1500,
            torque=50,
            tool_wear=100
        )

        assert False, "Expected ValueError"

    except ValueError:
        assert True


def test_negative_torque():

    try:

        predict_machine_failure(
            machine_type="L",
            air_temperature=300,
            process_temperature=310,
            rotational_speed=1500,
            torque=-10,
            tool_wear=100
        )

        assert False, "Expected ValueError"

    except ValueError:
        assert True


def test_out_of_range_reading_is_flagged():

    result = predict_machine_failure(
        machine_type="L",
        air_temperature=320,
        process_temperature=310,
        rotational_speed=1500,
        torque=50,
        tool_wear=100
    )

    assert result["input_supported"] is False
    assert result["out_of_range_features"] == ["Air temperature [K]"]
    assert result["possible_failure_modes"] == []
    assert 0 <= result["failure_probability"] <= 1


def test_medium_risk_prediction():

    result = predict_machine_failure(
        machine_type="L",
        air_temperature=300.5,
        process_temperature=309.8,
        rotational_speed=1345,
        torque=62.7,
        tool_wear=153
    )

    assert result["risk_level"] == "Medium Risk"
    assert result["predicted_failure"] == 0


def test_high_risk_prediction():

    result = predict_machine_failure(
        machine_type="L",
        air_temperature=298.9,
        process_temperature=310.2,
        rotational_speed=2737,
        torque=8.8,
        tool_wear=142
    )

    assert result["risk_level"] == "High Risk"
    assert result["predicted_failure"] == 1