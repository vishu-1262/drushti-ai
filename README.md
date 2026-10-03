# DRUSHTI AI

## Industrial Machine Failure Prediction & Predictive Maintenance

DRUSHTI AI is an end-to-end machine learning application designed to estimate the probability of industrial machine failure from operating conditions.

The system combines machine learning, data preprocessing, a prediction API, automated testing, and an interactive dashboard into one complete application.

> DRUSHTI AI is a decision-support system. Its prediction is a model-based probability estimate, not a guarantee that a machine will fail.

---

## Problem Statement

Unexpected machine failures can lead to:

- Production downtime
- Maintenance costs
- Equipment damage
- Production delays
- Reduced operational efficiency

Traditional maintenance approaches often depend on scheduled maintenance, manual inspection, or fixed thresholds.

DRUSHTI AI explores how machine learning can use multiple operating conditions together to estimate machine failure risk.

---

## Project Objective

Given the current operating conditions of a machine, DRUSHTI AI predicts:

1. Failure probability
2. Predicted failure status
3. Risk level

### Input Features

- Machine Type
- Air Temperature
- Process Temperature
- Rotational Speed
- Torque
- Tool Wear

### Output

```text
Failure Probability
Predicted Failure
Risk Level
```

## Run Locally

Install the project dependencies in your virtual environment:

```powershell
python -m pip install -r requirements.txt
```

Open two PowerShell terminals from the project folder. Start the prediction API in the first:

```powershell
python -m uvicorn app.main:app --reload
```

Start the Streamlit frontend in the second:

```powershell
python -m streamlit run app/frontend.py
```

The frontend is available at `http://localhost:8501`. The API must remain running while making predictions.

## Deploy on Render

The frontend and API are separate services. Deploy both from this GitHub repository in the same region.

### 1. Deploy the API

Create a **Web Service** connected to this repository with:

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `DRUSHTI_DATABASE_PATH=/var/data/machine_records.sqlite3`

Add a persistent disk mounted at `/var/data`, then deploy the service. The disk is important: without persistent storage, saved machine history and service reminders can disappear when the service restarts. Keep the API to one running instance while using SQLite.

After deployment, copy the API service URL, for example `https://your-api-name.onrender.com`.

### 2. Deploy the frontend

Create a second **Web Service** from the same repository with:

- Build command: `pip install -r requirements.txt`
- Start command: `streamlit run app/frontend.py --server.address 0.0.0.0 --server.port $PORT --server.headless true`
- Environment variable: `DRUSHTI_API_URL=https://your-api-name.onrender.com`

Use the actual API URL from step 1, including `https://`, then deploy. Open the frontend URL provided by Render.

### 3. Verify the deployment

Open `https://your-api-name.onrender.com/health`; it should return a healthy status. Then enter a machine ID in the frontend, save a maintenance reminder, and run a prediction. Confirm that the result appears in Recent readings and remains there after refreshing the page.

Hosting persistent disks may require a paid plan. If you deploy without one, the app can run, but its SQLite history and reminders are not guaranteed to survive restarts. Do not put real production machine data into this demo without appropriate access controls, backups, and operational validation.

## Machine History and Maintenance

Enter a machine ID before analyzing it. Predictions are saved locally in `data/machine_records.sqlite3` and shown in that machine's recent-reading history.

In **Maintenance reminder**, enter the last service date and how many days should pass between services. The app shows when the next service is due. These reminders are based on the schedule entered by the user, not an automatic diagnosis.

For supported readings, the app can show failure types found among the five closest labeled failure examples in the AI4I dataset. These are suggestions for inspection, not confirmation that a particular part is faulty. Readings outside the model's training ranges do not show these suggestions.

## Model Limitations

The saved model was checked on 2,000 held-back AI4I examples. It found 49 of 68 failures, missed 19, and raised 9 false alarms. This benchmark result has not been validated against live factory machines. Treat the displayed score as an estimate, not a guarantee.

Risk labels use score bands: Low below 5%, Medium from 5% to below 50%, and High at 50% or above. In the held-back examples, observed failure rates were 0.3% in the Low band, 13.1% in Medium, and 84.5% in High. These are benchmark results, not promised real-world rates.