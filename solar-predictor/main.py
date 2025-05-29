from src.data_loader import get_data

def main():
    # Load data with automatic fallback to sample data creation
    train, test = get_data()
    
    print("Solar Predictor - Data Loaded Successfully!")
    print(f"Training data shape: {train.shape}")
    
    if test is not None:
        print(f"Test data shape: {test.shape}")
    
    # Display basic info about the dataset
    print("\nDataset Info:")
    print(train.info())
    
    print("\nFirst few rows:")
    print(train.head())
    
    print("\nBasic statistics:")
    print(train.describe())

if __name__ == "__main__":
    main()