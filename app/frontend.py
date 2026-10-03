from datetime import date
from html import escape
import os

import streamlit as st
import requests

try:
    configured_api_url = st.secrets.get("DRUSHTI_API_URL")
except st.errors.StreamlitSecretNotFoundError:
    configured_api_url = None

API_URL = (
    configured_api_url
    or os.getenv("DRUSHTI_API_URL")
    or "http://127.0.0.1:8000"
).rstrip("/")

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="DRUSHTI AI | Machine Intelligence",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #071525;
        color: #E8F1F8;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #06111F;
        border-right: 1px solid #17314A;
    }

    /* Brand */
    .brand {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.5px;
        color: #F4F8FB;
    }

    .brand span {
        color: #18C8E8;
    }

    .tagline {
        font-size: 12px;
        color: #8EA6B9;
        margin-top: -8px;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            135deg,
            #0B2035,
            #102C45
        );
        border: 1px solid #1C4564;
        border-radius: 18px;
        padding: 32px;
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero-title span {
        color: #19C7E8;
    }

    .hero-subtitle {
        color: #A7BBCB;
        font-size: 17px;
        line-height: 1.6;
        max-width: 700px;
    }

    .status {
        color: #31E58A;
        font-weight: 700;
        font-size: 14px;
    }

    /* Cards */
    .card {
        background: #0B1C2D;
        border: 1px solid #193A54;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 21px;
        font-weight: 700;
        color: #F1F6FA;
        margin-bottom: 4px;
    }

    .card-description {
        color: #8EA6B9;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Prediction */
    .prediction-card {
        background: linear-gradient(
            145deg,
            #092D30,
            #08242C
        );
        border: 1px solid #139B91;
        border-radius: 16px;
        padding: 26px;
    }

    .probability {
        font-size: 48px;
        font-weight: 800;
        color: #31E58A;
        text-align: center;
    }

    .probability-label {
        color: #8EA6B9;
        text-align: center;
        font-size: 14px;
    }

    .risk-low {
        background: #0E6B4D;
        color: #B8FFE0;
        padding: 12px 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: 800;
        font-size: 20px;
    }

    .risk-medium {
        background: #775A0B;
        color: #FFE8A3;
        padding: 12px 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: 800;
        font-size: 20px;
    }

    .risk-high {
        background: #762E35;
        color: #FFD1D5;
        padding: 12px 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: 800;
        font-size: 20px;
    }

    /* Recommendation */
    .recommendation {
        background: #0A2430;
        border: 1px solid #1A746F;
        border-radius: 12px;
        padding: 18px;
        margin-top: 20px;
    }

    .recommendation-title {
        color: #55E6A2;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .recommendation-text {
        color: #B8CBD8;
        font-size: 14px;
    }

    /* Workflow */
    .workflow {
        background: #0B1C2D;
        border: 1px solid #193A54;
        border-radius: 16px;
        padding: 24px;
    }

    .workflow-step {
        background: #10263A;
        border: 1px solid #23445C;
        border-radius: 12px;
        padding: 18px;
        text-align: center;
        height: 150px;
    }

    .workflow-number {
        color: #19C7E8;
        font-size: 13px;
        font-weight: 700;
    }

    .workflow-title {
        font-weight: 700;
        margin-top: 8px;
    }

    .workflow-text {
        color: #8EA6B9;
        font-size: 12px;
        margin-top: 6px;
    }

    /* Feature list */
    .feature {
        color: #B8CBD8;
        padding: 8px 0;
        font-size: 14px;
    }

    .feature span {
        color: #31E58A;
        margin-right: 8px;
    }

    /* Button */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 48px;
        font-size: 16px;
        font-weight: 700;
        border: none;
        background: linear-gradient(
            90deg,
            #168CF5,
            #18D6B2
        );
        color: white;
    }

    .stButton > button:hover {
        border: none;
        color: white;
        transform: translateY(-1px);
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] {
        background: #10263A;
        color: white;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        '<div class="brand">⚙ DRUSHTI <span>AI</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tagline">See risk before it becomes reality</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🏠 Home")
    st.markdown("### 📊 Machine Assessment")
    st.markdown("### ℹ️ About")

    st.divider()

    st.html(
        """
        <div style="color:#8EA6B9;font-size:13px;line-height:1.6;">
        <b>DRUSHTI AI</b> is an ML-powered predictive
        maintenance decision-support system designed
        to estimate machine failure risk.
        </div>
        """
    )


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.html("""
<div class="hero">

    <div class="status">● SYSTEM READY</div>

    <div class="hero-title">
        DRUSHTI <span>AI</span>
    </div>

    <div style="font-size:23px;font-weight:600;margin-bottom:10px;">
        Industrial Machine Failure Prediction
    </div>

    <div class="hero-subtitle">
        AI-powered insights for smarter maintenance,
        reduced downtime, and more reliable industrial operations.
    </div>

</div>
""")


# ---------------------------------------------------------
# INPUT + RESULT
# ---------------------------------------------------------

input_col, result_col = st.columns([1, 1], gap="large")


# ---------------------------------------------------------
# INPUT PANEL
# ---------------------------------------------------------

with input_col:

    st.html("""
    <div class="card">

        <div class="card-title">
            ⚙️ Machine Information
        </div>

        <div class="card-description">
            Enter the current operating conditions of the machine.
        </div>

    </div>
    """)

    machine_id = st.text_input(
        "Machine ID",
        value="MACHINE-001",
        max_chars=80,
    )

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"],
        format_func=lambda x: {
            "L": "L — Low",
            "M": "M — Medium",
            "H": "H — High"
        }[x]
    )

    air_temperature = st.number_input(
        "Air Temperature (K)",
        min_value=250.0,
        max_value=400.0,
        value=300.0,
        step=0.1
    )

    process_temperature = st.number_input(
        "Process Temperature (K)",
        min_value=250.0,
        max_value=450.0,
        value=310.0,
        step=0.1
    )

    rotational_speed = st.number_input(
        "Rotational Speed (rpm)",
        min_value=0.0,
        max_value=5000.0,
        value=1500.0,
        step=10.0
    )

    torque = st.number_input(
        "Torque (Nm)",
        min_value=0.0,
        max_value=500.0,
        value=50.0,
        step=1.0
    )

    tool_wear = st.number_input(
        "Tool Wear (min)",
        min_value=0.0,
        max_value=500.0,
        value=100.0,
        step=1.0
    )

    with st.expander("Maintenance reminder"):
        saved_schedule = None
        if machine_id.strip():
            try:
                schedule_response = requests.get(
                    f"{API_URL}/machines/{machine_id.strip()}/maintenance",
                    timeout=5,
                )
                if schedule_response.ok:
                    schedule_data = schedule_response.json()
                    if schedule_data.get("configured") is not False:
                        saved_schedule = schedule_data
            except requests.RequestException:
                pass

        last_service_default = date.today()
        interval_default = 90
        if saved_schedule:
            last_service_default = date.fromisoformat(
                saved_schedule["last_serviced_on"]
            )
            interval_default = saved_schedule["interval_days"]

        last_serviced_on = st.date_input(
            "Last serviced",
            value=last_service_default,
            max_value=date.today(),
        )
        maintenance_interval = st.number_input(
            "Remind me every (days)",
            min_value=1,
            max_value=3650,
            value=interval_default,
            step=1,
        )

        if st.button("Save reminder", key="save_maintenance"):
            if not machine_id.strip():
                st.error("Enter a machine ID before saving a reminder.")
            else:
                try:
                    schedule_response = requests.put(
                        f"{API_URL}/machines/{machine_id.strip()}/maintenance",
                        json={
                            "last_serviced_on": last_serviced_on.isoformat(),
                            "interval_days": int(maintenance_interval),
                        },
                        timeout=10,
                    )
                    if schedule_response.ok:
                        saved_schedule = schedule_response.json()
                    else:
                        st.error(schedule_response.json().get("detail", "Could not save reminder."))
                except requests.RequestException:
                    st.error("The prediction API is not running.")

        if saved_schedule:
            days_remaining = saved_schedule["days_remaining"]
            due_date = saved_schedule["due_date"]
            if days_remaining < 0:
                st.error(f"Maintenance is overdue by {abs(days_remaining)} days (due {due_date}).")
            elif days_remaining == 0:
                st.warning("Maintenance is due today.")
            elif days_remaining <= 7:
                st.warning(f"Maintenance is due in {days_remaining} days ({due_date}).")
            else:
                st.success(f"Next maintenance is due {due_date}.")
        else:
            st.caption("Set a service date and interval to create a reminder for this machine.")

    analyze = st.button("🔍 ANALYZE MACHINE")


# ---------------------------------------------------------
# RESULT PANEL
# ---------------------------------------------------------

with result_col:

    st.html("""
    <div class="prediction-card">

        <div class="card-title">
            📈 Prediction Result
        </div>

        <div class="card-description">
            Based on the trained machine-learning model.
        </div>

    """)

    if analyze and machine_id.strip():

        payload = {
            "machine_id": machine_id.strip(),
            "machine_type": machine_type,
            "air_temperature": air_temperature,
            "process_temperature": process_temperature,
            "rotational_speed": rotational_speed,
            "torque": torque,
            "tool_wear": tool_wear
        }
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()

                probability = result["failure_probability"]
                predicted_failure = result["predicted_failure"]
                risk_level = result["risk_level"]

                probability_percent = probability * 100

                st.html(
                    f"""
                    <div class="probability">
                        {probability_percent:.2f}%
                    </div>

                    <div class="probability-label">
                        Failure Probability
                    </div>
                    """
                )

                if result["input_supported"]:
                    st.caption(
                        "All readings are within the values seen in the "
                        "training examples."
                    )
                else:
                    unusual_readings = ", ".join(
                        result["out_of_range_features"]
                    )
                    st.warning(
                        "These readings are outside the values in the "
                        f"training examples: {unusual_readings}. "
                        "The prediction may be less reliable. Check the "
                        "measurements before acting."
                    )

                if result["possible_failure_modes"]:
                    with st.expander("Possible areas to inspect"):
                        st.caption(
                            "These are similar labeled failures from the "
                            "example dataset, not a confirmed diagnosis."
                        )
                        for mode in result["possible_failure_modes"]:
                            st.write(
                                f"**{mode['name']}** appeared in "
                                f"{mode['similar_examples']} of "
                                f"{mode['examples_checked']} nearby examples."
                            )

                validation = result["model_validation"]
                with st.expander("How much should I trust this estimate?"):
                    st.write(
                        f"On {validation['test_examples']:,} held-back "
                        f"{validation['dataset']} examples, the model found "
                        f"{validation['detected_failures']} of "
                        f"{validation['test_failures']} failures and missed "
                        f"{validation['missed_failures']}. It also raised "
                        f"{validation['false_alarms']} false alarms."
                    )
                    st.caption(
                        f"That is {validation['recall_percent']}% of failures "
                        f"caught and {validation['precision_percent']}% "
                        "precision on benchmark data. This has not been "
                        "validated against your factory's machines."
                    )
                    st.caption(
                        "Score bands: Low below 5%, Medium 5% to below 50%, "
                        "High 50% or above. In that test, observed failure "
                        f"rates were {validation['risk_bands']['low']['observed_failure_percent']}% "
                        f"Low, {validation['risk_bands']['medium']['observed_failure_percent']}% "
                        f"Medium, and {validation['risk_bands']['high']['observed_failure_percent']}% High."
                    )

                if risk_level == "Low Risk":

                    st.markdown(
                        '<div class="risk-low">✓ LOW RISK</div>',
                        unsafe_allow_html=True
                    )

                    recommendation = (
                        "Continue operation and monitor machine conditions."
                    )

                elif risk_level == "Medium Risk":

                    st.markdown(
                        '<div class="risk-medium">⚠ MEDIUM RISK</div>',
                        unsafe_allow_html=True
                    )

                    recommendation = (
                        "Schedule an inspection and monitor the machine closely."
                    )

                else:

                    st.markdown(
                        '<div class="risk-high">⚠ HIGH RISK</div>',
                        unsafe_allow_html=True
                    )

                    recommendation = (
                        "Prioritize inspection and consider maintenance action."
                    )

                st.html(
                    f"""
                    <div style="margin-top:20px;line-height:2;">

                    <b>Predicted Failure:</b>
                    {"Yes" if predicted_failure == 1 else "No"}

                    <br>

                    <b>Risk Level:</b>
                    {risk_level}

                    </div>

                    <div class="recommendation">

                        <div class="recommendation-title">
                            💡 Maintenance Recommendation
                        </div>

                        <div class="recommendation-text">
                            {recommendation}
                        </div>

                    </div>
                    """
                )

            else:

                st.error(
                    f"API returned an error: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "DRUSHTI AI API is not running. "
                "Start FastAPI first."
            )

        except Exception as e:

            st.error(f"Unexpected error: {e}")

    else:

        if analyze and not machine_id.strip():
            st.error("Enter a machine ID before analyzing the machine.")
        else:
            st.info(
                "Enter machine operating conditions and click "
                "**Analyze Machine** to generate a prediction."
            )


if machine_id.strip():
    st.markdown("## Recent readings")
    st.caption(f"Saved readings for {machine_id.strip()}")
    try:
        history_response = requests.get(
            f"{API_URL}/machines/{machine_id.strip()}/history",
            timeout=5,
        )
        if history_response.ok:
            machine_history = history_response.json()
            if machine_history:
                history_rows = "".join(
                    "<tr>"
                    f"<td>{escape(item['recorded_at'].replace('T', ' ')[:19])}</td>"
                    f"<td>{escape(item['machine_type'])}</td>"
                    f"<td>{item['air_temperature']:.1f} K</td>"
                    f"<td>{item['process_temperature']:.1f} K</td>"
                    f"<td>{item['rotational_speed']:.0f} rpm</td>"
                    f"<td>{item['torque']:.1f} Nm</td>"
                    f"<td>{item['tool_wear']:.0f} min</td>"
                    f"<td>{item['failure_probability']:.2%}</td>"
                    f"<td>{escape(item['risk_level'])}</td>"
                    "</tr>"
                    for item in machine_history
                )
                st.html(
                    "<div style='overflow-x:auto'><table "
                    "style='width:100%;border-collapse:collapse;white-space:nowrap'>"
                    "<thead><tr>"
                    "<th>Recorded</th><th>Type</th><th>Air</th>"
                    "<th>Process</th><th>Speed</th><th>Torque</th>"
                    "<th>Tool wear</th><th>Failure estimate</th><th>Risk</th>"
                    f"</tr></thead><tbody>{history_rows}</tbody></table></div>"
                )
            else:
                st.caption("No readings saved for this machine yet.")
        else:
            st.caption("Reading history is currently unavailable.")
    except requests.RequestException:
        st.caption("Start the prediction API to view saved machine readings.")

# ---------------------------------------------------------
# WORKFLOW
# ---------------------------------------------------------

st.markdown("##")

st.html("""
<div class="workflow">

    <div class="card-title">
        ⚙️ How DRUSHTI AI Works
    </div>

    <div class="card-description">
        From machine data to actionable maintenance insight.
    </div>

</div>
""")


w1, w2, w3, w4 = st.columns(4)

workflow = [
    (
        w1,
        "01",
        "Machine Data",
        "Temperature, speed, torque and tool wear."
    ),
    (
        w2,
        "02",
        "Preprocessing",
        "Data is validated and prepared."
    ),
    (
        w3,
        "03",
        "ML Model",
        "Model estimates machine failure probability."
    ),
    (
        w4,
        "04",
        "Risk Result",
        "Probability converted into an actionable risk level."
    )
]

for column, number, title, description in workflow:

    with column:

        st.html(
            f"""
            <div class="workflow-step">

                <div class="workflow-number">
                    STEP {number}
                </div>

                <div class="workflow-title">
                    {title}
                </div>

                <div class="workflow-text">
                    {description}
                </div>

            </div>
            """
        )


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------

st.markdown("##")

feature_col, about_col = st.columns(2, gap="large")


with feature_col:

    st.html("""
    <div class="card">

        <div class="card-title">
            ✦ Key Features
        </div>

        <div class="feature">
            <span>✓</span> Machine health assessment
        </div>

        <div class="feature">
            <span>✓</span> Failure probability prediction
        </div>

        <div class="feature">
            <span>✓</span> Risk-based maintenance guidance
        </div>

        <div class="feature">
            <span>✓</span> Machine-learning prediction pipeline
        </div>

        <div class="feature">
            <span>✓</span> FastAPI prediction service
        </div>

    </div>
    """)


with about_col:

    st.html("""
    <div class="card">

        <div class="card-title">
            🧠 About DRUSHTI AI
        </div>

        <div class="card-description">
            DRUSHTI AI is an explainable predictive-maintenance
            decision-support system.
        </div>

        <div style="color:#B8CBD8;font-size:14px;line-height:1.8;">

            It uses machine operating conditions to estimate
            the probability of failure and provide a simple
            risk assessment for maintenance teams.

            <br><br>

            <b>Important:</b> A predicted probability is an
            estimate from the trained model, not a guarantee
            that a machine will fail.

        </div>

    </div>
    """)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.html("""
<div style="
    text-align:center;
    color:#60798D;
    font-size:12px;
    padding:30px 0 10px 0;
">
    DRUSHTI AI • Industrial Machine Intelligence
    <br>
    ML-powered predictive maintenance decision support
</div>
""")