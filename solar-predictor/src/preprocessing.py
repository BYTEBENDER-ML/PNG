import pandas as pd

def preprocess_data(train, test=None):
    # Training features/target
    X = train[['temperature', 'humidity', 'wind_speed',
               'irradiance', 'panel_efficiency', 'system_size']]
    y = train['output_kWh']  # or 'efficiency'

    if test is not None:
        test_X = test[['temperature', 'humidity', 'wind_speed',
                       'irradiance', 'panel_efficiency', 'system_size']]
        test_ids = test['id']
        return X, y, test_X, test_ids
    else:
        return X, y

