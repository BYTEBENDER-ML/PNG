from src.data_loader import load_data
from src.preprocessing import preprocess
from src.model import train_model
import pandas as pd
import joblib
import os

# Step 1: Load data
train, test = load_data()

# Step 2: Preprocess and extract features
X, y, test_X, test_ids = preprocess(train, test)

# Step 3: Train model and save it
model = train_model(X, y)

# Step 4: Make predictions on test set
preds = model.predict(test_X)

# Step 5: Save predictions to submission.csv
submission = pd.DataFrame({
    'id': test_ids,
    'efficiency': preds.round(4)
})

# Ensure 'submission.csv' is written to project root
submission_path = os.path.join(os.getcwd(), 'submission.csv')
submission.to_csv(submission_path, index=False)

print(f"\n[SUCCESS] Submission file saved to: {submission_path}")