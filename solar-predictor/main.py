import pandas as pd
from preprocessing import preprocess_data           # Your custom preprocessing function
from src.model import train_model                   # Your model training function

# --- Load Datasets ---
train_df = pd.read_csv("train.csv")                 # Must contain 'efficiency' column
test_df = pd.read_csv("test.csv")                   # Should match structure of train.csv

# --- Preprocess Training Data ---
X_train, y_train, train_columns = preprocess_data(train_df)

# --- Preprocess Test Data (align columns with training data) ---
X_test, test_ids = preprocess_data(
    test_df, is_test=True, fit_columns=train_columns
)

# --- Train Model ---
model = train_model(X_train, y_train)

# --- Make Predictions on Test Data ---
predictions = model.predict(X_test)

# --- Output ---
for idx, pred in zip(test_ids, predictions):
    print(f"ID: {idx}, Predicted Efficiency: {pred:.4f}")
