# src/preprocessing.py
from sklearn.preprocessing import LabelEncoder

def preprocess(train, test):
    y = train['efficiency']
    train = train.drop(['id', 'efficiency'], axis=1)
    test_ids = test['id']
    test = test.drop(['id'], axis=1)

    cat_cols = ['string_id', 'error_code', 'installation_type']
    le = LabelEncoder()
    for col in cat_cols:
        train[col] = le.fit_transform(train[col])
        test[col] = le.transform(test[col])

    return train, y, test, test_ids
