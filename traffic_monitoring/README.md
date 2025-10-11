# Traffic Monitoring System using Machine Learning

A complete machine learning system for predicting vehicle counts based on time of day, day of week, and weather conditions. This project includes data generation, model training, evaluation, and inference capabilities.

## 🚗 Project Overview

This traffic monitoring system uses a Random Forest regression model to predict vehicle counts at traffic monitoring points. The model is trained on 2000 synthetic data samples that simulate realistic traffic patterns including:
- Rush hour peaks (7-9 AM, 5-7 PM)
- Weekend traffic variations
- Weather impact on traffic flow

## 📊 Model Performance

- **Training Set MAE**: 3.34 vehicles
- **Test Set MAE**: 4.24 vehicles
- **R² Score**: 0.43 (test set)
- **Dataset Size**: 2000 samples (80% train, 20% test)

### Feature Importance
1. **Hour of day** (58.2%) - Most significant factor
2. **Day of week** (24.2%) - Weekday vs weekend patterns
3. **Weather conditions** (17.6%) - Rainy, sunny, cloudy

## 🚀 Quick Start

### 1. Generate Synthetic Dataset
```bash
python traffic_monitoring/data_generator.py
```
Generates 2000 traffic samples with features: hour, day_of_week, weather, and vehicle_count.

### 2. Train the Model
```bash
python traffic_monitoring/model.py
```
Trains a Random Forest model and saves it as `traffic_model.joblib`.

### 3. Evaluate Model Performance
```bash
python traffic_monitoring/evaluate.py
```
Displays detailed metrics, feature importance, and sample predictions.

### 4. Run Predictions
```bash
python traffic_monitoring/inference.py
```
Tests the model with different traffic scenarios (rush hour, late night, weekends).

## 📁 Project Structure

```
traffic_monitoring/
├── data_generator.py    # Synthetic data generation (2000 samples)
├── model.py            # Model training script
├── evaluate.py         # Model evaluation and metrics
├── inference.py        # Prediction script
├── traffic_data.csv    # Generated dataset (after running data_generator.py)
├── traffic_model.joblib # Trained model (after running model.py)
└── README.md           # This file
```

## 🔧 Requirements

- Python 3.7+
- pandas
- numpy
- scikit-learn
- joblib
- matplotlib (optional, for visualization)

Install all dependencies:
```bash
pip install pandas numpy scikit-learn joblib matplotlib
```

## 💡 Usage Examples

### Custom Predictions

Modify `inference.py` or create your own script:

```python
from inference import predict

# Predict for Monday morning rush hour, rainy weather
sample = {'hour': 8, 'day_of_week': 1, 'weather': 'rainy'}
vehicle_count = predict(sample)
print(f"Predicted vehicles: {vehicle_count}")
```

### Understanding the Features

- **hour**: 0-23 (24-hour format)
- **day_of_week**: 0-6 (Monday=0, Sunday=6)
- **weather**: 'sunny', 'rainy', or 'cloudy'

## 📈 Model Details

- **Algorithm**: Random Forest Regressor
- **Number of Trees**: 100
- **Training Samples**: 1600
- **Test Samples**: 400
- **Validation**: 80/20 train-test split

## 🎯 Use Cases

1. Traffic flow prediction for road planning
2. Smart traffic signal timing optimization
3. Parking management systems
4. Urban transportation planning
5. Emergency route planning

## 🔮 Future Enhancements

- Real-time data integration
- Deep learning models (LSTM for time series)
- Multi-location traffic prediction
- Traffic camera image analysis
- API endpoint for predictions
- Dashboard visualization

## 📝 License

This project is open source and available for educational purposes.

## 👥 Contributing

Feel free to fork, modify, and enhance this traffic monitoring system!
