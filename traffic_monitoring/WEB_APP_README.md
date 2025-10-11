# 🌐 Traffic Monitoring System - Web Interface

## Quick Start

### Run the Web Application:
```bash
python traffic_monitoring/app.py
```

Then open your browser and go to:
**http://localhost:5000**

## Features

### 🎯 Interactive Prediction
- Select hour, day, and weather
- Get instant traffic predictions
- Quick presets for common scenarios (Morning Rush, Afternoon, Evening Rush)

### 📊 Real-time Statistics
- Total dataset samples
- Average traffic count
- Peak and minimum traffic
- Weather impact analysis with visual charts

### 🎨 Beautiful UI
- Modern gradient design
- Responsive layout (works on mobile)
- Smooth animations
- Easy-to-use interface

## How to Use

1. **Start the Server**:
   ```bash
   python traffic_monitoring/app.py
   ```

2. **Open Browser**:
   - Navigate to `http://localhost:5000`

3. **Make Predictions**:
   - Use quick presets OR
   - Manually select:
     - Hour (0-23)
     - Day of week (Monday-Sunday)
     - Weather (Sunny/Cloudy/Rainy)
   - Click "Predict Traffic"
   - See results instantly!

4. **View Statistics**:
   - See dataset statistics in real-time
   - View weather impact charts
   - Monitor system performance

## API Endpoints

### `GET /`
- Home page with prediction form

### `POST /predict`
- Make a traffic prediction
- **Request Body**:
  ```json
  {
    "hour": 8,
    "day_of_week": 1,
    "weather": "sunny"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "prediction": 28,
    "hour": 8,
    "day": "Monday",
    "weather": "Sunny"
  }
  ```

### `GET /stats`
- Get system statistics
- **Response**:
  ```json
  {
    "success": true,
    "total_samples": 2000,
    "avg_traffic": 21.57,
    "max_traffic": 46,
    "min_traffic": 2,
    "hourly_average": {...},
    "daily_average": {...},
    "weather_average": {...}
  }
  ```

## Requirements

- Python 3.7+
- Flask
- pandas
- numpy
- scikit-learn
- joblib

Install all:
```bash
pip install -r requirements.txt
```

## Stopping the Server

Press `CTRL+C` in the terminal to stop the server.

## Customization

### Change Port
Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
```

### Modify UI
Edit `templates/index.html` to customize:
- Colors
- Layout
- Content
- Styles

### Add Features
You can extend `app.py` with:
- More API endpoints
- Database integration
- User authentication
- Historical data tracking
- Export functionality

## Screenshots

### Main Interface
- Clean, modern design
- Two-column layout
- Prediction form on left
- Statistics on right

### Features
- 🌅 Quick preset buttons
- 🎨 Gradient backgrounds
- 📊 Visual charts
- 🚗 Real-time predictions

## Troubleshooting

**Port already in use**:
```bash
# Change port in app.py or kill the process using port 5000
```

**Model not found**:
```bash
# Train the model first
python traffic_monitoring/model.py
```

**Flask not installed**:
```bash
pip install flask
```

## Production Deployment

For production, consider:
- Using Gunicorn or uWSGI
- Setting `debug=False`
- Adding HTTPS
- Using a reverse proxy (Nginx)
- Implementing rate limiting
- Adding authentication

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

**Enjoy your traffic monitoring web application!** 🚦🌐
