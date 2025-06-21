import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Dict, Any, Optional
import joblib
import warnings

from preprocessing import preprocess_data           # Your custom preprocessing function
from src.model import train_model                   # Your model training function

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_preprocessing_artifacts(scaler, encoders, columns, output_dir: str = "artifacts"):
    """Save preprocessing artifacts for later use."""
    Path(output_dir).mkdir(exist_ok=True)
    
    if scaler:
        joblib.dump(scaler, f"{output_dir}/scaler.pkl")
        logger.info(f"Scaler saved to {output_dir}/scaler.pkl")
    
    if encoders:
        joblib.dump(encoders, f"{output_dir}/label_encoders.pkl")
        logger.info(f"Label encoders saved to {output_dir}/label_encoders.pkl")
    
    if columns:
        joblib.dump(columns, f"{output_dir}/feature_columns.pkl")
        logger.info(f"Feature columns saved to {output_dir}/feature_columns.pkl")

def load_preprocessing_artifacts(artifacts_dir: str = "artifacts"):
    """Load preprocessing artifacts."""
    try:
        scaler = joblib.load(f"{artifacts_dir}/scaler.pkl")
        encoders = joblib.load(f"{artifacts_dir}/label_encoders.pkl")
        columns = joblib.load(f"{artifacts_dir}/feature_columns.pkl")
        logger.info("Preprocessing artifacts loaded successfully")
        return scaler, encoders, columns
    except FileNotFoundError as e:
        logger.warning(f"Preprocessing artifacts not found: {e}")
        return None, None, None

def validate_data(df: pd.DataFrame, dataset_name: str) -> bool:
    """Validate input data quality."""
    logger.info(f"Validating {dataset_name} data...")
    
    if df.empty:
        logger.error(f"{dataset_name} dataset is empty")
        return False
    
    # Check for required columns
    required_cols = ['id', 'temperature', 'irradiance', 'humidity', 'panel_age']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.warning(f"Missing recommended columns in {dataset_name}: {missing_cols}")
    
    # Check data types and ranges
    if 'efficiency' in df.columns:
        efficiency_range = df['efficiency'].describe()
        logger.info(f"Efficiency range in {dataset_name}: {efficiency_range['min']:.4f} to {efficiency_range['max']:.4f}")
        
        # Check for unrealistic efficiency values
        if efficiency_range['min'] < 0 or efficiency_range['max'] > 1:
            logger.warning("Efficiency values outside expected range [0, 1] detected")
    
    # Check for duplicate IDs
    if 'id' in df.columns:
        duplicate_ids = df['id'].duplicated().sum()
        if duplicate_ids > 0:
            logger.warning(f"Found {duplicate_ids} duplicate IDs in {dataset_name}")
    
    logger.info(f"{dataset_name} validation completed. Shape: {df.shape}")
    return True

def create_submission_file(test_ids: pd.Series, predictions: np.ndarray, 
                          filename: str = "submission.csv") -> None:
    """Create submission file in standard format."""
    submission_df = pd.DataFrame({
        'id': test_ids,
        'efficiency': predictions
    })
    
    # Round predictions to reasonable precision
    submission_df['efficiency'] = submission_df['efficiency'].round(6)
    
    # Ensure efficiency is within valid range
    submission_df['efficiency'] = submission_df['efficiency'].clip(0, 1)
    
    submission_df.to_csv(filename, index=False)
    logger.info(f"Submission file saved as {filename}")
    logger.info(f"Prediction statistics:")
    logger.info(f"  Mean: {predictions.mean():.6f}")
    logger.info(f"  Std: {predictions.std():.6f}")
    logger.info(f"  Min: {predictions.min():.6f}")
    logger.info(f"  Max: {predictions.max():.6f}")

def main(
    train_path: str = "train.csv",
    test_path: str = "test.csv",
    use_cached_artifacts: bool = False,
    save_artifacts: bool = True,
    create_submission: bool = True
):
    """
    Main training and prediction pipeline.
    
    Parameters:
        train_path: Path to training CSV file
        test_path: Path to test CSV file
        use_cached_artifacts: Whether to use previously saved preprocessing artifacts
        save_artifacts: Whether to save preprocessing artifacts
        create_submission: Whether to create submission CSV file
    """
    
    try:
        # --- Load Datasets ---
        logger.info("Loading datasets...")
        
        if not Path(train_path).exists():
            raise FileNotFoundError(f"Training file not found: {train_path}")
        if not Path(test_path).exists():
            raise FileNotFoundError(f"Test file not found: {test_path}")
        
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        
        logger.info(f"Training data shape: {train_df.shape}")
        logger.info(f"Test data shape: {test_df.shape}")
        
        # Validate datasets
        if not (validate_data(train_df, "training") and validate_data(test_df, "test")):
            logger.error("Data validation failed")
            return
        
        # Check for target column in training data
        if 'efficiency' not in train_df.columns:
            raise ValueError("Training data must contain 'efficiency' column")
        
        # --- Load or Create Preprocessing Artifacts ---
        scaler, encoders, fit_columns = None, None, None
        if use_cached_artifacts:
            scaler, encoders, fit_columns = load_preprocessing_artifacts()
        
        # --- Preprocess Training Data ---
        logger.info("Preprocessing training data...")
        
        preprocessing_params = {
            'handle_outliers': True,
            'outlier_method': 'iqr'
        }
        
        X_train, y_train, fitted_scaler, fitted_encoders = preprocess_data(
            train_df, 
            is_test=False,
            **preprocessing_params
        )
        
        # Use newly fitted artifacts if not using cached ones
        if not use_cached_artifacts:
            scaler = fitted_scaler
            encoders = fitted_encoders
            fit_columns = X_train.columns.tolist()
        
        logger.info(f"Training features shape: {X_train.shape}")
        logger.info(f"Training target shape: {y_train.shape}")
        
        # --- Preprocess Test Data ---
        logger.info("Preprocessing test data...")
        
        # Store test IDs before preprocessing
        test_ids = test_df['id'].copy() if 'id' in test_df.columns else pd.Series(range(len(test_df)))
        
        X_test, _, _, _ = preprocess_data(
            test_df,
            is_test=True,
            fit_columns=fit_columns,
            scaler=scaler,
            label_encoders=encoders,
            **preprocessing_params
        )
        
        logger.info(f"Test features shape: {X_test.shape}")
        
        # Verify column alignment
        if list(X_train.columns) != list(X_test.columns):
            logger.warning("Training and test columns don't match perfectly")
            logger.info(f"Training columns: {len(X_train.columns)}")
            logger.info(f"Test columns: {len(X_test.columns)}")
        
        # --- Save Preprocessing Artifacts ---
        if save_artifacts and not use_cached_artifacts:
            save_preprocessing_artifacts(scaler, encoders, fit_columns)
        
        # --- Train Model ---
        logger.info("Training model...")
        
        model = train_model(X_train, y_train)
        
        if hasattr(model, 'feature_importances_'):
            # Log feature importance for tree-based models
            feature_importance = pd.DataFrame({
                'feature': X_train.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            logger.info("Top 10 most important features:")
            for idx, row in feature_importance.head(10).iterrows():
                logger.info(f"  {row['feature']}: {row['importance']:.4f}")
        
        # --- Make Predictions on Test Data ---
        logger.info("Making predictions...")
        
        predictions = model.predict(X_test)
        
        # Basic prediction validation
        if np.any(np.isnan(predictions)):
            logger.warning("NaN values detected in predictions, replacing with median")
            predictions = np.nan_to_num(predictions, nan=np.nanmedian(predictions))
        
        # --- Output Results ---
        logger.info("Prediction Results:")
        logger.info("-" * 50)
        
        # Display sample predictions
        sample_size = min(10, len(predictions))
        for i in range(sample_size):
            logger.info(f"ID: {test_ids.iloc[i]}, Predicted Efficiency: {predictions[i]:.6f}")
        
        if len(predictions) > sample_size:
            logger.info(f"... and {len(predictions) - sample_size} more predictions")
        
        # --- Create Submission File ---
        if create_submission:
            create_submission_file(test_ids, predictions)
        
        logger.info("Pipeline completed successfully!")
        
        return {
            'model': model,
            'predictions': predictions,
            'test_ids': test_ids,
            'scaler': scaler,
            'encoders': encoders,
            'feature_columns': fit_columns
        }
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Run the main pipeline
    results = main(
        train_path="train.csv",
        test_path="test.csv",
        use_cached_artifacts=False,  # Set to True to reuse saved preprocessing artifacts
        save_artifacts=True,         # Save preprocessing artifacts for future use
        create_submission=True       # Create submission.csv file
    )
    
    # Additional analysis or model saving can be done here
    if results:
        # Save the trained model
        joblib.dump(results['model'], 'trained_model.pkl')
        logger.info("Trained model saved as 'trained_model.pkl'")