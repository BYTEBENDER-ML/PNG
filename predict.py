def simulate_realtime_prediction():
    while True:
        input_data = get_random_input()
        pred_efficiency = model.predict(input_data)[0]
        
        print(f"Predicted Efficiency: {pred_efficiency:.2f}")
        
        if pred_efficiency < 60:
            print("⚠️  ALERT: Possible degradation detected.")
        
        time.sleep(2)  # simulate 2-second sensor delay