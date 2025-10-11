import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

def load_data(path='traffic_data.csv'):
    df = pd.read_csv(path)
    # One-hot encode weather
    df = pd.get_dummies(df, columns=['weather'])
    X = df.drop('vehicle_count', axis=1)
    y = df['vehicle_count']
    return X, y

def train_model():
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'traffic_data.csv')
    model_path = os.path.join(script_dir, 'traffic_model.joblib')
    
    X, y = load_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f'Training on {len(X_train)} samples, testing on {len(X_test)} samples...')
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f'Mean Absolute Error: {mae:.2f}')
    
    joblib.dump(model, model_path)
    print(f'Model saved to {model_path}')

if __name__ == '__main__':
    train_model()
