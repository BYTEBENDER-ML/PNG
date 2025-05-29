import pandas as pd

FEATURES = [
    'id', 'temperature', 'irradiance', 'humidity', 'panel_age',
    'maintenance_count', 'soiling_ratio', 'voltage', 'current',
    'module_temperature', 'cloud_coverage', 'wind_speed', 'pressure',
    'string_id', 'error_code', 'installation_type'
]

def preprocess_data(df, is_test=False, fit_columns=None):
    df = df.copy()
    
    # If training, extract target
    if not is_test:
        y = df['efficiency']
    else:
        y = None

    # Keep only needed columns
    columns_to_keep = FEATURES + (['efficiency'] if not is_test else [])
    df = df[columns_to_keep]
    
    df = df.fillna("missing")
    df = pd.get_dummies(df, columns=['string_id', 'error_code', 'installation_type'])
    df = df.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Align with training columns
    if is_test and fit_columns is not None:
        df = df.reindex(columns=fit_columns, fill_value=0)

    if not is_test:
        X = df.drop(columns=['efficiency'])
        return X, y, X.columns  # return columns for test alignment
    else:
        return df, df['id'] if 'id' in df else None

