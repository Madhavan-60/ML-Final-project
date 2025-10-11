"""
Visualize traffic patterns from the dataset and model predictions
"""
import pandas as pd
import numpy as np
import os

def visualize_patterns():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'traffic_data.csv')
    
    df = pd.read_csv(data_path)
    
    print("=" * 70)
    print("TRAFFIC PATTERNS ANALYSIS")
    print("=" * 70)
    
    # Average by hour
    print("\n1. Average Vehicle Count by Hour of Day:")
    print("-" * 70)
    hourly_avg = df.groupby('hour')['vehicle_count'].mean().sort_index()
    for hour, count in hourly_avg.items():
        bar = '█' * int(count / 2)
        print(f"  {hour:02d}:00 | {bar} {count:.1f}")
    
    # Average by day
    print("\n2. Average Vehicle Count by Day of Week:")
    print("-" * 70)
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_avg = df.groupby('day_of_week')['vehicle_count'].mean().sort_index()
    for day_num, count in daily_avg.items():
        bar = '█' * int(count / 2)
        print(f"  {days[day_num]:12s} | {bar} {count:.1f}")
    
    # Average by weather
    print("\n3. Average Vehicle Count by Weather:")
    print("-" * 70)
    weather_avg = df.groupby('weather')['vehicle_count'].mean().sort_values(ascending=False)
    for weather, count in weather_avg.items():
        bar = '█' * int(count / 2)
        print(f"  {weather.capitalize():12s} | {bar} {count:.1f}")
    
    # Peak hours
    print("\n4. Top 5 Peak Traffic Hours:")
    print("-" * 70)
    peak_hours = df.groupby('hour')['vehicle_count'].mean().sort_values(ascending=False).head(5)
    for i, (hour, count) in enumerate(peak_hours.items(), 1):
        print(f"  {i}. {hour:02d}:00 - Average: {count:.1f} vehicles")
    
    # Low traffic hours
    print("\n5. Top 5 Lowest Traffic Hours:")
    print("-" * 70)
    low_hours = df.groupby('hour')['vehicle_count'].mean().sort_values().head(5)
    for i, (hour, count) in enumerate(low_hours.items(), 1):
        print(f"  {i}. {hour:02d}:00 - Average: {count:.1f} vehicles")
    
    # Weather impact
    print("\n6. Weather Impact on Traffic:")
    print("-" * 70)
    base = df.groupby('weather')['vehicle_count'].mean()
    for weather in base.index:
        diff = base[weather] - base.mean()
        symbol = "+" if diff > 0 else ""
        print(f"  {weather.capitalize():12s}: {symbol}{diff:.2f} vehicles vs average")
    
    # Rush hour analysis
    print("\n7. Rush Hour Analysis:")
    print("-" * 70)
    morning_rush = df[df['hour'].between(7, 9)]['vehicle_count'].mean()
    evening_rush = df[df['hour'].between(17, 19)]['vehicle_count'].mean()
    off_peak = df[~df['hour'].between(7, 9) & ~df['hour'].between(17, 19)]['vehicle_count'].mean()
    
    print(f"  Morning Rush (7-9 AM):    {morning_rush:.1f} vehicles")
    print(f"  Evening Rush (5-7 PM):    {evening_rush:.1f} vehicles")
    print(f"  Off-Peak Hours:           {off_peak:.1f} vehicles")
    print(f"  Rush Hour Increase:       +{((morning_rush + evening_rush) / 2 - off_peak):.1f} vehicles")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    visualize_patterns()
