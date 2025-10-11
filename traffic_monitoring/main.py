"""
Traffic Monitoring System - Main Runner
This script executes the complete pipeline: data generation, training, evaluation, and inference.
"""
import os
import sys

def run_pipeline():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("TRAFFIC MONITORING SYSTEM - ML PIPELINE")
    print("=" * 70)
    
    # Step 1: Generate Data
    print("\n[STEP 1/4] Generating synthetic traffic data (2000 samples)...")
    print("-" * 70)
    from data_generator import generate_traffic_data, save_data
    save_data(os.path.join(script_dir, 'traffic_data.csv'))
    
    # Step 2: Train Model
    print("\n[STEP 2/4] Training Random Forest model...")
    print("-" * 70)
    from model import train_model
    train_model()
    
    # Step 3: Evaluate Model
    print("\n[STEP 3/4] Evaluating model performance...")
    print("-" * 70)
    from evaluate import evaluate_model
    evaluate_model()
    
    # Step 4: Run Inference
    print("\n[STEP 4/4] Running sample predictions...")
    print("-" * 70)
    from inference import predict
    
    test_cases = [
        {'hour': 8, 'day_of_week': 1, 'weather': 'rainy', 'description': 'Monday morning, rainy (rush hour)'},
        {'hour': 17, 'day_of_week': 3, 'weather': 'sunny', 'description': 'Wednesday evening, sunny (rush hour)'},
        {'hour': 14, 'day_of_week': 5, 'weather': 'cloudy', 'description': 'Friday afternoon, cloudy'},
        {'hour': 2, 'day_of_week': 6, 'weather': 'cloudy', 'description': 'Saturday night, cloudy (low traffic)'},
        {'hour': 11, 'day_of_week': 0, 'weather': 'sunny', 'description': 'Sunday morning, sunny'},
    ]
    
    print("\nTraffic Predictions for Various Scenarios:")
    print("=" * 70)
    for i, sample in enumerate(test_cases, 1):
        desc = sample.pop('description', '')
        pred = predict(sample)
        print(f"\n{i}. {desc}")
        print(f"   Hour: {sample['hour']:02d}:00, Day: {sample['day_of_week']}, Weather: {sample['weather']}")
        print(f"   → Predicted vehicle count: {pred}")
    
    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nFiles created:")
    print(f"  - traffic_data.csv (dataset)")
    print(f"  - traffic_model.joblib (trained model)")
    print("\nYou can now use inference.py for custom predictions.")

if __name__ == '__main__':
    try:
        run_pipeline()
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
