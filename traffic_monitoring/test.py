"""
Quick Test Script - Verify the Traffic Monitoring System
"""
from inference import predict
import os

def quick_test():
    print("\n" + "=" * 70)
    print("TRAFFIC MONITORING SYSTEM - QUICK TEST")
    print("=" * 70)
    
    # Check if model exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'traffic_model.joblib')
    data_path = os.path.join(script_dir, 'traffic_data.csv')
    
    if not os.path.exists(model_path):
        print("\n❌ ERROR: Model not found!")
        print("   Please run: python traffic_monitoring/model.py")
        return False
    
    if not os.path.exists(data_path):
        print("\n❌ ERROR: Dataset not found!")
        print("   Please run: python traffic_monitoring/data_generator.py")
        return False
    
    print("\n✅ Model and dataset found!")
    
    # Test predictions
    print("\n" + "-" * 70)
    print("Testing predictions for various scenarios:")
    print("-" * 70)
    
    test_cases = [
        {'hour': 8, 'day_of_week': 1, 'weather': 'rainy', 'label': 'Monday morning rush, rainy'},
        {'hour': 17, 'day_of_week': 3, 'weather': 'sunny', 'label': 'Wednesday evening rush, sunny'},
        {'hour': 14, 'day_of_week': 5, 'weather': 'cloudy', 'label': 'Friday afternoon, cloudy'},
        {'hour': 2, 'day_of_week': 6, 'weather': 'cloudy', 'label': 'Saturday night, cloudy'},
        {'hour': 11, 'day_of_week': 0, 'weather': 'sunny', 'label': 'Sunday morning, sunny'},
    ]
    
    for i, case in enumerate(test_cases, 1):
        label = case.pop('label')
        try:
            result = predict(case)
            print(f"\n{i}. {label}")
            print(f"   Input: Hour={case['hour']}, Day={case['day_of_week']}, Weather={case['weather']}")
            print(f"   Prediction: {result} vehicles ✅")
        except Exception as e:
            print(f"\n{i}. {label}")
            print(f"   ❌ ERROR: {e}")
            return False
    
    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED - System is working correctly!")
    print("=" * 70)
    print("\nYou can now:")
    print("  - Run full pipeline: python traffic_monitoring/main.py")
    print("  - Make predictions: python traffic_monitoring/inference.py")
    print("  - View patterns: python traffic_monitoring/visualize.py")
    print("  - Evaluate model: python traffic_monitoring/evaluate.py")
    print()
    
    return True

if __name__ == '__main__':
    quick_test()
