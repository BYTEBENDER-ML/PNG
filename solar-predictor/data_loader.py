import pandas as pd
import os

def load_data():
    # Define the correct path
    data_path = r'C:\Users\rudra\.vscode\PNG\solar-predictor\data'
    train_file = os.path.join(data_path, 'train.csv')
    test_file = os.path.join(data_path, 'test.csv')
    
    # Check if files exist
    if not os.path.exists(train_file):
        raise FileNotFoundError(f"Training data not found at: {train_file}")
    
    if not os.path.exists(test_file):
        print(f"Warning: Test data not found at: {test_file}")
        test = None
    else:
        test = pd.read_csv(test_file)
    
    # Load the training data
    train = pd.read_csv(train_file)
    
    return train, test

# Alternative approach using relative path (recommended)
def load_data_relative():
    # This assumes your script is running from the solar-predictor directory
    train_file = 'data/train.csv'
    test_file = 'data/test.csv'
    
    if not os.path.exists(train_file):
        # Try absolute path as fallback
        base_path = r'C:\Users\rudra\.vscode\PNG\solar-predictor'
        train_file = os.path.join(base_path, 'data', 'train.csv')
        test_file = os.path.join(base_path, 'data', 'test.csv')
    
    if not os.path.exists(train_file):
        raise FileNotFoundError(f"Training data not found. Checked paths:\n- data/train.csv\n- {train_file}")
    
    train = pd.read_csv(train_file)
    test = pd.read_csv(test_file) if os.path.exists(test_file) else None
    
    return train, test

# If you need to create sample data for testing
def create_sample_data():
    import numpy as np
    
    data_path = r'C:\Users\rudra\.vscode\PNG\solar-predictor\data'
    
    # Create directory if it doesn't exist
    os.makedirs(data_path, exist_ok=True)
    
    # Create sample solar prediction data
    np.random.seed(42)  # For reproducible results
    n_samples = 1000
    
    sample_data = pd.DataFrame({
        'solar_irradiance': np.random.uniform(0, 1200, n_samples),
        'temperature': np.random.uniform(10, 45, n_samples),
        'humidity': np.random.uniform(20, 95, n_samples),
        'wind_speed': np.random.uniform(0, 20, n_samples),
        'cloud_cover': np.random.uniform(0, 100, n_samples),
        'power_output': np.random.uniform(0, 6000, n_samples)  # Target variable
    })
    
    # Split into train and test
    train_data = sample_data[:800]
    test_data = sample_data[800:]
    
    # Save to CSV files
    train_data.to_csv(os.path.join(data_path, 'train.csv'), index=False)
    test_data.to_csv(os.path.join(data_path, 'test.csv'), index=False)
    
    print(f"Sample data created at: {data_path}")
    print(f"Training samples: {len(train_data)}")
    print(f"Test samples: {len(test_data)}")

# Main function to use in your code
def get_data():
    try:
        return load_data_relative()
    except FileNotFoundError as e:
        print(f"Data files not found: {e}")
        print("Creating sample data...")
        create_sample_data()
        return load_data_relative()

if __name__ == "__main__":
    # Test the data loader
    train, test = get_data()
    print("Data loaded successfully!")
    print(f"Training data shape: {train.shape}")
    if test is not None:
        print(f"Test data shape: {test.shape}")
    print("\nTraining data preview:")
    print(train.head())