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