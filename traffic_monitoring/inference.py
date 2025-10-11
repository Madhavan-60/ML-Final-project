import pandas as pd
import joblib
import os

def predict(input_dict, model_path=None):
    if model_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'traffic_model.joblib')
    
    model = joblib.load(model_path)
    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df)
    # Ensure all columns match training
    for col in ['weather_cloudy', 'weather_rainy', 'weather_sunny']:
        if col not in df:
            df[col] = 0
    df = df[['hour', 'day_of_week', 'weather_cloudy', 'weather_rainy', 'weather_sunny']]
    pred = model.predict(df)[0]
    return int(pred)

if __name__ == '__main__':
    # Example predictions for different scenarios
    test_cases = [
        {'hour': 8, 'day_of_week': 1, 'weather': 'rainy', 'description': 'Monday morning, rainy (rush hour)'},
        {'hour': 17, 'day_of_week': 3, 'weather': 'sunny', 'description': 'Wednesday evening, sunny (rush hour)'},
        {'hour': 2, 'day_of_week': 6, 'weather': 'cloudy', 'description': 'Saturday night, cloudy (low traffic)'},
    ]
    
    print("Traffic Monitoring System - Predictions:")
    print("=" * 60)
    for i, sample in enumerate(test_cases, 1):
        desc = sample.pop('description', '')
        pred = predict(sample)
        print(f"\nTest {i}: {desc}")
        print(f"  Hour: {sample['hour']}, Day: {sample['day_of_week']}, Weather: {sample['weather']}")
        print(f"  -> Predicted vehicle count: {pred}")
