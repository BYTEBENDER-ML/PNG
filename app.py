import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
from pathlib import Path

st.set_page_config(
        page_title="Solar Energy Predictor",
        page_icon="🌞",
        layout="wide"
    )

# Import your existing modules
try:
    from src.model import train_model, make_prediction
    from src.preprocessing import preprocess_data
except ImportError:
    st.error("Could not import src modules. Make sure src/ directory exists with model.py and preprocessing.py")

def load_or_train_model():
    """Load existing model or train new one"""
    model_path = 'models/solar_model.pkl'
    
    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            return model, "Loaded existing model"
        except Exception as e:
            st.error(f"Error loading model: {e}")
            return None, f"Error: {e}"
    else:
        # Train new model
        try:
            # Load data
            if os.path.exists('data/solar_data.csv'):
                data = pd.read_csv('data/solar_data.csv')
                X, y = preprocess_data(data)
                model = train_model(X, y)
                
                # Save model
                os.makedirs('models', exist_ok=True)
                joblib.dump(model, model_path)
                
                return model, "Trained and saved new model"
            else:
                return None, "No data file found"
        except Exception as e:
            return None, f"Training error: {e}"

def main():
    
    
    st.title("🌞 Solar Energy Predictor")
    st.markdown("---")
    
    # Sidebar for model management
    st.sidebar.header("Model Management")
    
    # Load or train model
    if st.sidebar.button("Load/Train Model"):
        with st.spinner("Loading/Training model..."):
            model, status = load_or_train_model()
            st.sidebar.success(status)
            
            # Store model in session state
            if model is not None:
                st.session_state.model = model
    
    # Check if model exists in session state
    if 'model' not in st.session_state:
        st.warning("Please load or train a model first using the sidebar.")
        return
    
    # Main prediction interface
    st.header("Make Predictions")
    
    # Create input form
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Environmental Conditions")
        temperature = st.slider("Temperature (°C)", -10, 50, 25)
        humidity = st.slider("Humidity (%)", 0, 100, 50)
        wind_speed = st.slider("Wind Speed (km/h)", 0, 50, 10)
        
    with col2:
        st.subheader("System Parameters")
        solar_irradiance = st.slider("Solar Irradiance (W/m²)", 0, 1000, 500)
        panel_efficiency = st.slider("Panel Efficiency (%)", 10, 25, 20)
        system_size = st.slider("System Size (kW)", 1, 100, 10)
    
    # Prediction button
    if st.button("Predict Solar Energy Output", type="primary"):
        try:
            # Prepare input data (adjust based on your model's expected features)
            input_data = np.array([[
                temperature, humidity, wind_speed, 
                solar_irradiance, panel_efficiency, system_size
            ]])
            
            # Make prediction
            prediction = st.session_state.model.predict(input_data)[0]
            
            # Display results
            st.success(f"🔋 Predicted Solar Energy Output: **{prediction:.2f} kWh**")
            
            # Display input summary
            st.subheader("Input Summary")
            input_summary = pd.DataFrame({
                'Parameter': [
                    'Temperature', 'Humidity', 'Wind Speed',
                    'Solar Irradiance', 'Panel Efficiency', 'System Size'
                ],
                'Value': [
                    f"{temperature}°C", f"{humidity}%", f"{wind_speed} km/h",
                    f"{solar_irradiance} W/m²", f"{panel_efficiency}%", f"{system_size} kW"
                ]
            })
            st.table(input_summary)
            
        except Exception as e:
            st.error(f"Prediction error: {e}")
    
    # Model information
    st.markdown("---")
    st.subheader("Model Information")
    
    if os.path.exists('models/solar_model.pkl'):
        model_stats = os.stat('models/solar_model.pkl')
        st.info(f"Model last updated: {pd.to_datetime(model_stats.st_mtime, unit='s')}")
    
    # Data upload section
    st.markdown("---")
    st.subheader("Batch Predictions")
    
    uploaded_file = st.file_uploader("Upload CSV for batch predictions", type=['csv'])
    
    if uploaded_file is not None:
        try:
            batch_data = pd.read_csv(uploaded_file)
            st.write("Uploaded data preview:")
            st.dataframe(batch_data.head())
            
            if st.button("Run Batch Predictions"):
                # Process batch predictions (adjust based on your preprocessing)
                predictions = st.session_state.model.predict(batch_data)
                
                # Add predictions to dataframe
                batch_data['Predicted_Output'] = predictions
                
                st.write("Predictions completed:")
                st.dataframe(batch_data)
                
                # Download results
                csv = batch_data.to_csv(index=False)
                st.download_button(
                    label="Download Results",
                    data=csv,
                    file_name="solar_predictions.csv",
                    mime="text/csv"
                )
                
        except Exception as e:
            st.error(f"Batch prediction error: {e}")

# Training interface (optional separate page)
def training_page():
    st.title("🔧 Model Training")
    
    uploaded_data = st.file_uploader("Upload training data", type=['csv'])
    
    if uploaded_data is not None:
        data = pd.read_csv(uploaded_data)
        st.write("Data preview:")
        st.dataframe(data.head())
        
        if st.button("Train New Model"):
            with st.spinner("Training model..."):
                try:
                    X, y = preprocess_data(data)
                    model = train_model(X, y)
                    
                    # Save model
                    os.makedirs('models', exist_ok=True)
                    joblib.dump(model, 'models/solar_model.pkl')
                    
                    st.success("Model trained and saved successfully!")
                    st.session_state.model = model
                    
                except Exception as e:
                    st.error(f"Training failed: {e}")

# Navigation
def create_navigation():
    pages = {
        "Prediction": main,
        "Training": training_page
    }
    
    selected_page = st.sidebar.selectbox("Navigate", list(pages.keys()))
    pages[selected_page]()

if __name__ == "__main__":
    # Use navigation or just main
    # create_navigation()  # Uncomment for multi-page app
    main()  # Comment this if using navigation