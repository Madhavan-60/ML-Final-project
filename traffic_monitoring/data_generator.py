import numpy as np
import pandas as pd

def generate_traffic_data(num_samples=30000, random_state=42):
    """Generate traffic data with 30,000 samples"""
    np.random.seed(random_state)
    print(f"Generating {num_samples:,} traffic samples...")
    
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
    
    print(f"✓ Successfully generated {len(df):,} samples")
    return df

def save_data(filename='traffic_data.csv'):
    df = generate_traffic_data(num_samples=30000)
    df.to_csv(filename, index=False)
    print(f'✓ Saved {len(df):,} samples to {filename}')
    print(f'✓ File size: {len(df)} rows x {len(df.columns)} columns')

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_data(os.path.join(script_dir, 'traffic_data.csv'))
