import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import numpy as np

from sklearn.ensemble import RandomForestRegressor

def train_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

    X = X[selected_features]

    # Train-validation split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

    # Train model
    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)

    # Validation
    preds = model.predict(X_val)
    score = 100 * (1 - np.sqrt(mean_squared_error(y_val, preds)))
    print("Validation Score:", round(score, 2))

    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/solar_model.pkl')

    return model
