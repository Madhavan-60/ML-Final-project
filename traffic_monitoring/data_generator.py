import numpy as np
import pandas as pd

def generate_traffic_data(num_samples=2000, random_state=42):
    np.random.seed(random_state)
    # Simulate features: hour, day_of_week, weather, vehicle_count
    hours = np.random.randint(0, 24, num_samples)
    days = np.random.randint(0, 7, num_samples)
    weather = np.random.choice(['sunny', 'rainy', 'cloudy'], num_samples)
    # Simulate vehicle count based on hour, day, and weather
    base = 20 + 10 * (hours >= 7) * (hours <= 9) + 10 * (hours >= 17) * (hours <= 19)
    base += 5 * (days >= 5)  # weekends
    base += np.where(weather == 'rainy', -5, 0)
    vehicle_count = base + np.random.normal(0, 5, num_samples)
    vehicle_count = np.clip(vehicle_count, 0, None).astype(int)
    df = pd.DataFrame({
        'hour': hours,
        'day_of_week': days,
        'weather': weather,
        'vehicle_count': vehicle_count
    })
    return df

def save_data(filename='traffic_data.csv'):
    df = generate_traffic_data()
    df.to_csv(filename, index=False)
    print(f'Generated {len(df)} samples and saved to {filename}')

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_data(os.path.join(script_dir, 'traffic_data.csv'))
