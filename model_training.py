x_train, x_val, y_train, y_val = train_test_split(train, y, test_size=0.2, random_state=42)

model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42)
model.fit(x_train, y_train, eval_set=[(x_val, y_val)], early_stopping_rounds=10, verbose=False)
+