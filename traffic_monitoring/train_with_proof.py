"""
Traffic Monitoring Model - Training with 30,000 Samples
Comprehensive training script with detailed proof and metrics
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import time
from datetime import datetime
import json

print("=" * 80)
print("  TRAFFIC MONITORING MODEL - TRAINING WITH 30,000 SAMPLES")
print("=" * 80)
print()

# Step 1: Generate 30,000 training samples
print("📊 STEP 1: Generating 30,000 Traffic Data Samples")
print("-" * 80)

start_time = time.time()

np.random.seed(42)
data = []

hours = list(range(24)) * 1250  # 30,000 samples across all hours
np.random.shuffle(hours)

print("Generating samples with realistic traffic patterns...")
for i, hour in enumerate(hours):
    # Rush hour patterns
    if hour in [7, 8, 9, 17, 18, 19]:
        base_vehicles = np.random.randint(50, 100)
        cars = np.random.randint(30, 60)
        motorcycles = np.random.randint(10, 25)
        buses = np.random.randint(3, 8)
        trucks = np.random.randint(2, 7)
    # Off-peak hours
    elif hour in [0, 1, 2, 3, 4, 5]:
        base_vehicles = np.random.randint(5, 20)
        cars = np.random.randint(3, 12)
        motorcycles = np.random.randint(1, 5)
        buses = np.random.randint(0, 2)
        trucks = np.random.randint(1, 3)
    # Normal hours
    else:
        base_vehicles = np.random.randint(20, 50)
        cars = np.random.randint(12, 30)
        motorcycles = np.random.randint(5, 15)
        buses = np.random.randint(1, 5)
        trucks = np.random.randint(2, 5)
    
    # Weekend factor
    is_weekend = np.random.choice([0, 1], p=[5/7, 2/7])
    if is_weekend:
        base_vehicles = int(base_vehicles * 0.7)
        cars = int(cars * 0.8)
    
    # Weather factor
    weather = np.random.choice(['Clear', 'Rain', 'Fog'], p=[0.7, 0.2, 0.1])
    weather_factor = {'Clear': 1.0, 'Rain': 0.8, 'Fog': 0.6}
    base_vehicles = int(base_vehicles * weather_factor[weather])
    
    # Road type
    road_type = np.random.choice(['Highway', 'Urban', 'Suburban'], p=[0.3, 0.4, 0.3])
    
    # Average speed
    if base_vehicles > 70:
        avg_speed = np.random.randint(20, 40)
    elif base_vehicles > 40:
        avg_speed = np.random.randint(40, 60)
    else:
        avg_speed = np.random.randint(60, 90)
    
    data.append({
        'hour': hour,
        'is_weekend': is_weekend,
        'weather': weather,
        'road_type': road_type,
        'avg_speed': avg_speed,
        'cars': cars,
        'motorcycles': motorcycles,
        'buses': buses,
        'trucks': trucks,
        'total_vehicles': base_vehicles
    })
    
    # Progress indicator
    if (i + 1) % 5000 == 0:
        print(f"  Generated {i + 1:,} samples...")

df = pd.DataFrame(data)
df.to_csv('traffic_data_30k.csv', index=False)

generation_time = time.time() - start_time
print(f"\n✅ Generated 30,000 samples in {generation_time:.2f} seconds")
print(f"📁 Saved to: traffic_data_30k.csv")
print(f"📊 Dataset shape: {df.shape}")
print()

# Step 2: Data Analysis
print("📈 STEP 2: Dataset Analysis")
print("-" * 80)
print("\nDataset Statistics:")
print(df.describe())
print("\nData Distribution:")
print(f"  - Total samples: {len(df):,}")
print(f"  - Features: {len(df.columns) - 1}")
print(f"  - Target variable: total_vehicles")
print(f"  - Weekday samples: {len(df[df['is_weekend']==0]):,}")
print(f"  - Weekend samples: {len(df[df['is_weekend']==1]):,}")
print(f"\nWeather Distribution:")
print(df['weather'].value_counts())
print(f"\nRoad Type Distribution:")
print(df['road_type'].value_counts())
print(f"\nVehicle Statistics:")
print(f"  - Min vehicles: {df['total_vehicles'].min()}")
print(f"  - Max vehicles: {df['total_vehicles'].max()}")
print(f"  - Mean vehicles: {df['total_vehicles'].mean():.2f}")
print(f"  - Median vehicles: {df['total_vehicles'].median():.2f}")
print()

# Step 3: Prepare training data
print("🔧 STEP 3: Data Preprocessing")
print("-" * 80)

# One-hot encoding
df_encoded = pd.get_dummies(df, columns=['weather', 'road_type'], drop_first=False)
print(f"✅ Applied one-hot encoding")
print(f"   Total features after encoding: {len(df_encoded.columns) - 1}")

# Split features and target
X = df_encoded.drop('total_vehicles', axis=1)
y = df_encoded['total_vehicles']

print(f"✅ Split features (X) and target (y)")
print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"✅ Split into train/test sets (80/20)")
print(f"   Training samples: {len(X_train):,}")
print(f"   Testing samples: {len(X_test):,}")
print()

# Step 4: Train the model
print("🤖 STEP 4: Training Random Forest Model")
print("-" * 80)

training_start = time.time()

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

print("Model Configuration:")
print(f"  - Algorithm: Random Forest Regressor")
print(f"  - Number of trees: 100")
print(f"  - Max depth: 20")
print(f"  - Min samples split: 5")
print(f"  - Min samples leaf: 2")
print(f"  - Using all CPU cores: n_jobs=-1")
print("\nTraining in progress...")
print("-" * 80)

model.fit(X_train, y_train)

training_time = time.time() - training_start
print("-" * 80)
print(f"✅ Training completed in {training_time:.2f} seconds ({training_time/60:.2f} minutes)")
print()

# Step 5: Model Evaluation
print("📊 STEP 5: Model Evaluation & Performance Metrics")
print("-" * 80)

# Predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Training metrics
train_mae = mean_absolute_error(y_train, y_pred_train)
train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
train_r2 = r2_score(y_train, y_pred_train)

# Testing metrics
test_mae = mean_absolute_error(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
test_r2 = r2_score(y_test, y_pred_test)

print("\n🎯 TRAINING SET PERFORMANCE:")
print(f"  - MAE (Mean Absolute Error): {train_mae:.4f} vehicles")
print(f"  - RMSE (Root Mean Squared Error): {train_rmse:.4f} vehicles")
print(f"  - R² Score: {train_r2:.4f} ({train_r2*100:.2f}%)")

print("\n🎯 TESTING SET PERFORMANCE:")
print(f"  - MAE (Mean Absolute Error): {test_mae:.4f} vehicles")
print(f"  - RMSE (Root Mean Squared Error): {test_rmse:.4f} vehicles")
print(f"  - R² Score: {test_r2:.4f} ({test_r2*100:.2f}%)")

# Feature importance
print("\n🔍 TOP 10 MOST IMPORTANT FEATURES:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(10).iterrows():
    print(f"  {row['feature']:.<30} {row['importance']:.4f}")

# Step 6: Sample Predictions
print("\n🧪 STEP 6: Sample Predictions (Testing Accuracy)")
print("-" * 80)
print(f"{'Actual':>10} {'Predicted':>12} {'Error':>10} {'% Error':>12}")
print("-" * 80)

sample_indices = np.random.choice(len(y_test), 15, replace=False)
for idx in sample_indices:
    actual = y_test.iloc[idx]
    predicted = y_pred_test[idx]
    error = abs(actual - predicted)
    pct_error = (error / actual * 100) if actual > 0 else 0
    print(f"{actual:>10.1f} {predicted:>12.1f} {error:>10.2f} {pct_error:>11.2f}%")

avg_error_pct = np.mean([abs(y_test.iloc[i] - y_pred_test[i]) / y_test.iloc[i] * 100 
                          for i in range(len(y_test)) if y_test.iloc[i] > 0])
print("-" * 80)
print(f"Average Prediction Error: {avg_error_pct:.2f}%")
print()

# Step 7: Save the model
print("💾 STEP 7: Saving Model")
print("-" * 80)

joblib.dump(model, 'traffic_model.joblib')
print("✅ Model saved: traffic_model.joblib")

# Save feature names for prediction
with open('feature_names.json', 'w') as f:
    json.dump(list(X.columns), f)
print("✅ Feature names saved: feature_names.json")
print()

# Step 8: Generate Training Report
print("📝 STEP 8: Generating Training Report")
print("-" * 80)

report = {
    'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'dataset_size': len(df),
    'training_samples': len(X_train),
    'testing_samples': len(X_test),
    'features_count': len(X.columns),
    'training_time_seconds': round(training_time, 2),
    'data_generation_time_seconds': round(generation_time, 2),
    'model_parameters': {
        'n_estimators': 100,
        'max_depth': 20,
        'min_samples_split': 5,
        'min_samples_leaf': 2
    },
    'performance_metrics': {
        'train_mae': round(train_mae, 4),
        'train_rmse': round(train_rmse, 4),
        'train_r2': round(train_r2, 4),
        'test_mae': round(test_mae, 4),
        'test_rmse': round(test_rmse, 4),
        'test_r2': round(test_r2, 4),
        'avg_prediction_error_pct': round(avg_error_pct, 2)
    },
    'top_features': feature_importance.head(10).to_dict('records')
}

with open('training_report_30k.json', 'w', indent=4) as f:
    json.dump(report, f, indent=4)

print("✅ Training report saved: training_report_30k.json")
print()

# Final Summary
total_time = time.time() - start_time
print("=" * 80)
print("  ✅ TRAINING COMPLETE - SUMMARY")
print("=" * 80)
print(f"📊 Dataset: 30,000 samples")
print(f"🤖 Model: Random Forest (100 trees)")
print(f"⏱️  Total time: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
print(f"🎯 Test MAE: {test_mae:.4f} vehicles")
print(f"🎯 Test R² Score: {test_r2:.4f} ({test_r2*100:.2f}%)")
print(f"📈 Average Error: {avg_error_pct:.2f}%")
print()
print("📁 Files Generated:")
print("  - traffic_data_30k.csv (30,000 samples)")
print("  - traffic_model.joblib (trained model)")
print("  - feature_names.json (model features)")
print("  - training_report_30k.json (detailed report)")
print()
print("=" * 80)
print("  🎉 Model is ready for deployment!")
print("=" * 80)
