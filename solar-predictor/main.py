import pandas as pd
from preprocessing import preprocess_data
from src.model import train_model

# Load the dataset
train_df = pd.read_csv("train.csv")   # Make sure 'train.csv' exists in your directory
test_df = pd.read_csv("test.csv")     # Optional, for predictions

# Preprocess the data
X_train, y_train, train_columns = preprocess_data(train_df)
X_test, test_ids = preprocess_data(test_df, is_test=True, fit_columns=train_columns)

# Train the model
model = train_model(X_train, y_train)

# Predict on test data
preds = model.predict(X_test)

# Example output
print(preds)
