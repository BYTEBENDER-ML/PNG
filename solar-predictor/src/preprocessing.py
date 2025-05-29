from sklearn.preprocessing import LabelEncoder
import pandas as pd

def preprocess(train, test):
    # Separate target
    y = train['efficiency']
    train = train.drop(['id', 'efficiency'], axis=1)
    test_ids = test['id']
    test = test.drop(['id'], axis=1)

    # Encode categorical features
    cat_cols = ['string_id', 'error_code', 'installation_type']
    le = LabelEncoder()
    for col in cat_cols:
        train[col] = le.fit_transform(train[col].astype(str))
        test[col] = le.transform(test[col].astype(str))

    # Feature engineering
    train['power_output'] = train['voltage'] * train['current']
    test['power_output'] = test['voltage'] * test['current']

    train['temp_diff'] = train['module_temperature'] - train['temperature']
    test['temp_diff'] = test['module_temperature'] - test['temperature']

    train['maintenance_rate'] = train['maintenance_count'] / (train['panel_age'] + 0.1)
    test['maintenance_rate'] = test['maintenance_count'] / (test['panel_age'] + 0.1)

    # Force numeric conversion
    train = train.apply(pd.to_numeric, errors='coerce')
    test = test.apply(pd.to_numeric, errors='coerce')

    # Fill any resulting NaNs
    train.fillna(0, inplace=True)
    test.fillna(0, inplace=True)

    return train, y, test, test_ids
