# src/model.py
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import numpy as np
import joblib

def train_model(X, y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)
    
    preds = model.predict(X_val)
    score = 100 * (1 - np.sqrt(mean_squared_error(y_val, preds)))
    print(f"Validation Score: {score:.2f}")

    joblib.dump(model, 'models/solar_model.pkl')
    return model
