import streamlit as st
import pandas as pd
import joblib
import random

# Load trained model
model = joblib.load('models/solar_model.pkl')

# Simulate a single sensor data row
def simulate_sensor_data():
    return pd.DataFrame([{
        'temperature': random.uniform(20, 45),
        'irradiance': random.uniform(400, 1000),
        'humidity': random.uniform(10, 90),
        'panel_age': random.uniform(1, 10),
        'maintenance_count': random.randint(0, 5),
        'soiling_ratio': random.uniform(0.2, 1.0),
        'voltage': random.uniform(20, 40),
        'current': random.uniform(4, 12),
        'module_temperature': random.uniform(25, 60),
        'cloud_coverage': random.uniform(0, 100),
        'wind_speed': random.uniform(0, 10),
        'pressure': random.uniform(900, 1100),
        'string_id': 2,  # label encoded
        'error_code': 1,  # label encoded
        'installation_type': 0,  # label encoded
        'power_output': 0,  # will be calculated
        'temp_diff': 0,     # will be calculated
        'maintenance_rate': 0  # will be calculated
    }])

# Feature engineering
def engineer_features(df):
    df['power_output'] = df['voltage'] * df['current']
    df['temp_diff'] = df['module_temperature'] - df['temperature']
    df['maintenance_rate'] = df['maintenance_count'] / (df['panel_age'] + 0.1)
    return df

# Streamlit UI
st.title("🔆 Real-Time Solar Panel Efficiency Predictor")

if st.button("Simulate Sensor Input"):
    row = simulate_sensor_data()
    row = engineer_features(row)
    pred = model.predict(row)[0]
    st.write("### Simulated Sensor Data:")
    st.dataframe(row)
    st.write(f"### 🔋 Predicted Efficiency: `{pred:.2f}`")

    if pred < 60:
        st.error("⚠️ Degradation Alert! Low Efficiency Detected.")
    elif pred < 75:
        st.warning("⚠️ Performance Dropping. Consider Maintenance.")
    else:
        st.success("✅ Panel Operating Normally.")
