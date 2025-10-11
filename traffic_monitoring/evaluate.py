import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def evaluate_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'traffic_data.csv')
    model_path = os.path.join(script_dir, 'traffic_model.joblib')
    
    # Load data
    df = pd.read_csv(data_path)
    df = pd.get_dummies(df, columns=['weather'])
    X = df.drop('vehicle_count', axis=1)
    y = df['vehicle_count']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Load model
    model = joblib.load(model_path)
    
    # Make predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Calculate metrics
    print("=" * 60)
    print("TRAFFIC MONITORING SYSTEM - MODEL EVALUATION")
    print("=" * 60)
    print(f"\nDataset Information:")
    print(f"  Total samples: {len(df)}")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    
    print(f"\nTraining Set Performance:")
    print(f"  MAE (Mean Absolute Error): {mean_absolute_error(y_train, y_train_pred):.2f}")
    print(f"  RMSE (Root Mean Squared Error): {np.sqrt(mean_squared_error(y_train, y_train_pred)):.2f}")
    print(f"  R² Score: {r2_score(y_train, y_train_pred):.4f}")
    
    print(f"\nTest Set Performance:")
    print(f"  MAE (Mean Absolute Error): {mean_absolute_error(y_test, y_test_pred):.2f}")
    print(f"  RMSE (Root Mean Squared Error): {np.sqrt(mean_squared_error(y_test, y_test_pred)):.2f}")
    print(f"  R² Score: {r2_score(y_test, y_test_pred):.4f}")
    
    # Feature importance
    print(f"\nFeature Importance:")
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.iterrows():
        print(f"  {row['feature']}: {row['importance']:.4f}")
    
    print("\n" + "=" * 60)
    
    # Show sample predictions
    print("\nSample Predictions (first 10 test samples):")
    print("-" * 60)
    for i in range(min(10, len(y_test))):
        print(f"  Actual: {y_test.iloc[i]:3d}, Predicted: {int(y_test_pred[i]):3d}, Error: {abs(y_test.iloc[i] - y_test_pred[i]):.2f}")

if __name__ == '__main__':
    evaluate_model()
