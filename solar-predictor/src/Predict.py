import joblib
import pandas as pd
import os

# Check path
assert os.path.exists('models/solar_model.pkl'), "Model file missing!"
assert os.path.exists('data/test.csv'), "Test data file missing!"

# Load model
model = joblib.load('models/solar_model.pkl')

# Load test data
test = pd.read_csv('data/test.csv')

# Preprocess test if needed before prediction

# Predict
predictions = model.predict(test)

# Output
print(predictions)
