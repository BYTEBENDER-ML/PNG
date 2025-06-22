🔆 Solar Energy Prediction Project

👤 Author: Rudranshu Pandey

---

📌 Objective:
To build a machine learning model that predicts solar panel energy output based on 6 key features: temperature, humidity, wind speed, solar irradiance, panel efficiency, and system size.

---

🛠️ Tools & Libraries:
- Python 3.10
- XGBoost (regression)
- scikit-learn
- pandas, numpy
- Streamlit (for web UI)
- Joblib (for model saving)
- VS Code (dev environment)

---

📊 Feature Engineering:
- Selected 6 essential features to reduce complexity
- Removed irrelevant/complex fields from raw data
- Normalized missing values (if any) with `.fillna()`
- Ensured train and test used same column structure

---

🧠 ML Pipeline:
1. Load raw data using `data_loader.py`
2. Preprocess it using `preprocessing.py` (feature filtering)
3. Train an XGBoost model on selected features
4. Save the model using Joblib
5. Predict test set efficiency/output and generate `submission.csv`

---

🚀 Streamlit Web App (`app.py`):
- Allows manual input for real-time simulation
- Supports batch prediction from uploaded CSVs
- Displays predictions, alerts, and download options

---

📦 How to Run:
1. `pip install -r requirements.txt`
2. `python main.py` → to train and generate submission
3. `streamlit run app.py` → to launch the web interface

---

✅ Deliverables:
- Trained model (`models/solar_model.pkl`)
- Prediction output (`submission.csv`)
- Clean codebase with modular design
