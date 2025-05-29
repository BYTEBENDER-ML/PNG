test_preds = model.predict(test)

submission = pd.DataFrame({
    'id': test_ids,
    'efficiency': test_preds.round(4)
})
submission.to_csv('submission.csv', index=False)