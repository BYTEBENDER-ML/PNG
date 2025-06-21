# 🔆 Solar Panel Efficiency Predictor

This project predicts solar panel efficiency using historical and real-time sensor data, enabling proactive maintenance and improved energy output in solar systems.

## 🚀 Features

- Predicts performance degradation and failure risks
- Uses XGBoost for high-accuracy regression
- Feature-engineered inputs (e.g., power output, temp diff)
- Real-time simulation interface with Streamlit
- Submission-ready output for model evaluation

## 📁 Project Structure

solar-predictor/
├── data/ # Raw input files (train.csv, test.csv)
├── models/ # Trained model files (solar_model.pkl)
├── src/ # Code modules (preprocessing, training, loading)
├── submission.csv # Output prediction file
├── app.py # Streamlit app for live simulation
├── main.py # Main training + prediction script
└── README.md # Project documentation


## 📊 Dataset Overview

| Column Name        | Description                                           |
|--------------------|-------------------------------------------------------|
| temperature        | Ambient air temperature (°C)                          |
| irradiance         | Solar energy received per unit area (W/m²)           |
| humidity           | Relative humidity (%)                                 |
| panel_age          | Age of the solar panel in years                      |
| soiling_ratio      | Dust/debris factor (0 to 1)                           |
| voltage, current   | Electrical outputs                                    |
| error_code         | Logged fault codes (categorical)                     |
| installation_type  | Fixed / Tracking / Dual-axis                         |
| efficiency         | 📌 Target variable (predicted)                        |

## 🧠 ML Model

- **Model:** XGBoost Regressor
- **Features:** Numeric + Encoded Categorical + Engineered
- **Metric:**  
Score = 100 * (1 - sqrt(MSE(actual, predicted)))


## ▶️ How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt

2. Train the model and generate submission
python main.py

3. Launch the real-time simulation app
streamlit run app.py



