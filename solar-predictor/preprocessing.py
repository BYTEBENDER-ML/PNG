import pandas as pd
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from sklearn.preprocessing import StandardScaler, LabelEncoder
import warnings

# Define the features to keep
FEATURES = [
    'id', 'temperature', 'irradiance', 'humidity', 'panel_age',
    'maintenance_count', 'soiling_ratio', 'voltage', 'current',
    'module_temperature', 'cloud_coverage', 'wind_speed', 'pressure',
    'string_id', 'error_code', 'installation_type'
]

def preprocess_data(
    df: pd.DataFrame,
    is_test: bool = False,
    fit_columns: Optional[List[str]] = None,
    scaler: Optional[StandardScaler] = None,
    label_encoders: Optional[Dict[str, LabelEncoder]] = None,
    handle_outliers: bool = True,
    outlier_method: str = 'iqr'
) -> Tuple[pd.DataFrame, Optional[pd.Series], Optional[StandardScaler], Optional[Dict[str, LabelEncoder]]]:
    """
    Preprocesses the input DataFrame for training or testing with enhanced features.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        is_test (bool): Whether the data is test data (no target column).
        fit_columns (List[str], optional): Columns to align test data with training.
        scaler (StandardScaler, optional): Pre-fitted scaler for test data.
        label_encoders (Dict[str, LabelEncoder], optional): Pre-fitted label encoders.
        handle_outliers (bool): Whether to handle outliers in numerical features.
        outlier_method (str): Method for outlier detection ('iqr' or 'zscore').
    
    Returns:
        Tuple containing:
        - pd.DataFrame: Processed features
        - Optional[pd.Series]: Target variable (if training)
        - Optional[StandardScaler]: Fitted scaler (if training)
        - Optional[Dict[str, LabelEncoder]]: Fitted label encoders (if training)
    """
    df = df.copy()
    
    # Extract target if training
    y = None
    if not is_test and 'efficiency' in df.columns:
        y = df['efficiency'].copy()
        # Basic target validation
        if y.isnull().any():
            warnings.warn(f"Found {y.isnull().sum()} null values in target variable")
            y = y.fillna(y.median())

    # Keep relevant columns
    required_columns = FEATURES + (['efficiency'] if not is_test else [])
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in input DataFrame: {missing_cols}")
    
    # Drop efficiency from features
    feature_columns = [col for col in FEATURES if col in df.columns]
    df = df[feature_columns]

    # Separate numerical and categorical columns
    numerical_cols = ['temperature', 'irradiance', 'humidity', 'panel_age',
                     'maintenance_count', 'soiling_ratio', 'voltage', 'current',
                     'module_temperature', 'cloud_coverage', 'wind_speed', 'pressure']
    categorical_cols = ['string_id', 'error_code', 'installation_type']
    
    # Filter columns that actually exist in the dataframe
    numerical_cols = [col for col in numerical_cols if col in df.columns]
    categorical_cols = [col for col in categorical_cols if col in df.columns]

    # Handle missing values more intelligently
    for col in numerical_cols:
        if df[col].isnull().any():
            # Use median for numerical columns
            df[col] = df[col].fillna(df[col].median())
    
    for col in categorical_cols:
        if df[col].isnull().any():
            # Use mode for categorical columns, or 'unknown' if no mode exists
            mode_val = df[col].mode()
            fill_val = mode_val[0] if len(mode_val) > 0 else 'unknown'
            df[col] = df[col].fillna(fill_val)

    # Handle outliers in numerical columns (training only)
    if not is_test and handle_outliers and numerical_cols:
        df = _handle_outliers(df, numerical_cols, method=outlier_method)

    # Feature engineering
    df = _create_features(df, numerical_cols)

    # Handle categorical variables
    if not is_test:
        # Training: fit new label encoders
        fitted_encoders = {}
        for col in categorical_cols:
            le = LabelEncoder()
            # Handle unseen categories by adding them to classes_
            unique_vals = df[col].astype(str).unique()
            le.fit(unique_vals)
            df[col] = le.transform(df[col].astype(str))
            fitted_encoders[col] = le
    else:
        # Testing: use provided encoders
        fitted_encoders = label_encoders
        if fitted_encoders:
            for col in categorical_cols:
                if col in fitted_encoders:
                    # Handle unseen categories
                    le = fitted_encoders[col]
                    df[col] = df[col].astype(str)
                    # Map unseen categories to a default value (0 or most frequent)
                    df[col] = df[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                    df[col] = le.transform(df[col])

    # Convert all columns to numeric
    for col in df.columns:
        if col != 'id':  # Keep ID as is
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Scale numerical features
    if not is_test:
        # Training: fit new scaler
        fitted_scaler = StandardScaler()
        scale_cols = [col for col in df.columns if col not in ['id']]
        df[scale_cols] = fitted_scaler.fit_transform(df[scale_cols])
    else:
        # Testing: use provided scaler
        fitted_scaler = scaler
        if fitted_scaler:
            scale_cols = [col for col in df.columns if col not in ['id']]
            # Only scale columns that were in the training data
            available_cols = [col for col in scale_cols if col in fit_columns]
            if available_cols:
                df[available_cols] = fitted_scaler.transform(df[available_cols])

    # Align columns for test data
    if is_test and fit_columns is not None:
        # Add missing columns with zeros
        for col in fit_columns:
            if col not in df.columns:
                df[col] = 0
        # Reorder columns to match training data
        df = df.reindex(columns=fit_columns, fill_value=0)

    return df, y, fitted_scaler, fitted_encoders


def _handle_outliers(df: pd.DataFrame, numerical_cols: List[str], method: str = 'iqr') -> pd.DataFrame:
    """
    Handle outliers in numerical columns.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        numerical_cols (List[str]): List of numerical column names
        method (str): Method for outlier detection ('iqr' or 'zscore')
    
    Returns:
        pd.DataFrame: Dataframe with outliers handled
    """
    df_clean = df.copy()
    
    for col in numerical_cols:
        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Cap outliers instead of removing them
            df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
            
        elif method == 'zscore':
            mean_val = df_clean[col].mean()
            std_val = df_clean[col].std()
            z_scores = np.abs((df_clean[col] - mean_val) / std_val)
            
            # Cap values with z-score > 3
            outlier_mask = z_scores > 3
            if outlier_mask.any():
                lower_bound = mean_val - 3 * std_val
                upper_bound = mean_val + 3 * std_val
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
    
    return df_clean


def _create_features(df: pd.DataFrame, numerical_cols: List[str]) -> pd.DataFrame:
    """
    Create additional engineered features.
    
    Parameters:
        df (pd.DataFrame): Input dataframe
        numerical_cols (List[str]): List of numerical column names
    
    Returns:
        pd.DataFrame: Dataframe with additional features
    """
    df_enhanced = df.copy()
    
    # Power-related features
    if 'voltage' in df.columns and 'current' in df.columns:
        df_enhanced['power'] = df_enhanced['voltage'] * df_enhanced['current']
    
    # Temperature difference
    if 'temperature' in df.columns and 'module_temperature' in df.columns:
        df_enhanced['temp_diff'] = df_enhanced['module_temperature'] - df_enhanced['temperature']
    
    # Efficiency indicators
    if 'irradiance' in df.columns and 'voltage' in df.columns:
        df_enhanced['irradiance_voltage_ratio'] = df_enhanced['irradiance'] / (df_enhanced['voltage'] + 1e-8)
    
    # Environmental stress indicator
    env_cols = ['humidity', 'wind_speed', 'pressure']
    available_env_cols = [col for col in env_cols if col in df.columns]
    if len(available_env_cols) >= 2:
        df_enhanced['env_stress'] = df_enhanced[available_env_cols].std(axis=1)
    
    # Age-related degradation
    if 'panel_age' in df.columns and 'maintenance_count' in df.columns:
        df_enhanced['maintenance_frequency'] = df_enhanced['maintenance_count'] / (df_enhanced['panel_age'] + 1)
    
    return df_enhanced