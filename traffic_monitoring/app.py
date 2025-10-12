from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import joblib
import pandas as pd
import os
import cv2
import numpy as np
from datetime import datetime
from ultralytics import YOLO
from PIL import Image

app = Flask(__name__)

# Load YOLO model for vehicle detection
print("Loading YOLO model...")
yolo_model = YOLO('yolov8n.pt')  # Using YOLOv8 nano for speed
print("YOLO model loaded successfully!")

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create upload folder if it doesn't exist
script_dir = os.path.dirname(os.path.abspath(__file__))
upload_path = os.path.join(script_dir, UPLOAD_FOLDER)
os.makedirs(upload_path, exist_ok=True)

# Load the trained model
model_path = os.path.join(script_dir, 'traffic_model.joblib')
model = joblib.load(model_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_traffic(hour, day_of_week, weather):
    """Make a traffic prediction"""
    # Prepare input
    input_dict = {
        'hour': hour,
        'day_of_week': day_of_week,
        'weather': weather
    }
    
    df = pd.DataFrame([input_dict])
    df = pd.get_dummies(df)
    
    # Ensure all columns match training
    for col in ['weather_cloudy', 'weather_rainy', 'weather_sunny']:
        if col not in df:
            df[col] = 0
    
    df = df[['hour', 'day_of_week', 'weather_cloudy', 'weather_rainy', 'weather_sunny']]
    
    # Make prediction
    prediction = model.predict(df)[0]
    return int(prediction)

@app.route('/')
def home():
    """Home page with prediction form"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction request"""
    try:
        data = request.get_json()
        hour = int(data['hour'])
        day_of_week = int(data['day_of_week'])
        weather = data['weather']
        
        # Make prediction
        result = predict_traffic(hour, day_of_week, weather)
        
        # Get day name
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_name = days[day_of_week]
        
        return jsonify({
            'success': True,
            'prediction': result,
            'hour': hour,
            'day': day_name,
            'weather': weather.capitalize()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/stats')
def stats():
    """Get model statistics"""
    try:
        data_path = os.path.join(script_dir, 'traffic_data_30k.csv')
        df = pd.read_csv(data_path)
        
        # Calculate statistics
        hourly_avg = df.groupby('hour')['total_vehicles'].mean().to_dict()
        daily_avg = df.groupby('is_weekend')['total_vehicles'].mean().to_dict()
        weather_avg = df.groupby('weather')['total_vehicles'].mean().to_dict()
        
        # Calculate correlation matrix for numeric columns
        numeric_cols = ['hour', 'is_weekend', 'avg_speed', 'cars', 'motorcycles', 'buses', 'trucks', 'total_vehicles']
        correlation_matrix = df[numeric_cols].corr().to_dict()
        
        # Vehicle type breakdown
        vehicle_breakdown = {
            'cars': int(df['cars'].sum()),
            'motorcycles': int(df['motorcycles'].sum()),
            'buses': int(df['buses'].sum()),
            'trucks': int(df['trucks'].sum())
        }
        
        # Road type analysis
        road_type_avg = df.groupby('road_type')['total_vehicles'].mean().to_dict()
        
        # Speed vs traffic
        speed_ranges = pd.cut(df['avg_speed'], bins=[0, 20, 40, 60, 80, 100], labels=['0-20', '20-40', '40-60', '60-80', '80-100'])
        speed_traffic = df.groupby(speed_ranges)['total_vehicles'].mean().to_dict()
        speed_traffic = {str(k): v for k, v in speed_traffic.items() if pd.notna(k)}
        
        return jsonify({
            'success': True,
            'hourly_average': hourly_avg,
            'daily_average': daily_avg,
            'weather_average': weather_avg,
            'total_samples': len(df),
            'avg_traffic': float(df['total_vehicles'].mean()),
            'max_traffic': int(df['total_vehicles'].max()),
            'min_traffic': int(df['total_vehicles'].min()),
            'correlation_matrix': correlation_matrix,
            'vehicle_breakdown': vehicle_breakdown,
            'road_type_average': road_type_avg,
            'speed_traffic': speed_traffic
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/upload_video', methods=['POST'])
def upload_video():
    """Handle video upload and analysis"""
    try:
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No video file provided'})
        
        file = request.files['video']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if file and allowed_file(file.filename):
            # Secure filename
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(upload_path, filename)
            
            # Save file
            file.save(filepath)
            
            # Analyze video
            analysis_result = analyze_video(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'analysis': analysis_result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Allowed: MP4, AVI, MOV, MKV, WEBM'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def analyze_video(filepath):
    """Analyze traffic video using YOLO for vehicle detection with annotated frames"""
    try:
        cap = cv2.VideoCapture(filepath)
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Vehicle classes in COCO dataset (used by YOLO)
        vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
        vehicle_names = {2: 'car', 3: 'motorcycle', 5: 'bus', 7: 'truck'}
        
        # Colors for different vehicle types (BGR format)
        vehicle_colors = {
            2: (0, 255, 0),      # car - green
            3: (255, 0, 0),      # motorcycle - blue
            5: (0, 0, 255),      # bus - red
            7: (0, 255, 255)     # truck - yellow
        }
        
        # Sample frames for analysis
        vehicle_counts = []
        vehicle_types = {name: 0 for name in vehicle_names.values()}
        sample_frames = min(10, frame_count)  # Sample up to 10 frames for display
        frame_interval = max(1, frame_count // sample_frames)
        
        # Create unique folder for this video's detections
        video_id = os.path.splitext(os.path.basename(filepath))[0]
        detection_folder = os.path.join(script_dir, 'static', 'detections', video_id)
        os.makedirs(detection_folder, exist_ok=True)
        
        annotated_frames = []
        
        print(f"Analyzing video: {sample_frames} frames...")
        
        frame_idx = 0
        for i in range(0, frame_count, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if ret:
                # Make a copy for annotation
                annotated_frame = frame.copy()
                
                # Run YOLO detection
                results = yolo_model(frame, verbose=False)
                
                # Count vehicles in this frame
                frame_vehicle_count = 0
                detections_info = []
                
                for result in results:
                    boxes = result.boxes
                    for box in boxes:
                        cls = int(box.cls[0])
                        conf = float(box.conf[0])
                        
                        # Only process vehicles with confidence > 0.5
                        if cls in vehicle_classes and conf > 0.5:
                            frame_vehicle_count += 1
                            if cls in vehicle_names:
                                vehicle_types[vehicle_names[cls]] += 1
                            
                            # Get bounding box coordinates
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            
                            # Draw bounding box
                            color = vehicle_colors.get(cls, (255, 255, 255))
                            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 3)
                            
                            # Draw label with vehicle type and confidence
                            label = f"{vehicle_names.get(cls, 'vehicle')} {conf:.2f}"
                            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                            
                            # Draw label background
                            cv2.rectangle(annotated_frame, 
                                        (x1, y1 - label_size[1] - 10), 
                                        (x1 + label_size[0], y1), 
                                        color, -1)
                            
                            # Draw label text
                            cv2.putText(annotated_frame, label, 
                                      (x1, y1 - 5), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 
                                      0.6, (0, 0, 0), 2)
                            
                            detections_info.append({
                                'type': vehicle_names.get(cls, 'vehicle'),
                                'confidence': round(conf, 2),
                                'bbox': [x1, y1, x2, y2]
                            })
                
                # Add frame info overlay
                info_text = f"Frame {i}/{frame_count} | Vehicles: {frame_vehicle_count}"
                cv2.putText(annotated_frame, info_text, 
                          (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 
                          1, (255, 255, 255), 2)
                cv2.putText(annotated_frame, info_text, 
                          (10, 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 
                          1, (0, 0, 0), 1)
                
                # Save annotated frame
                frame_filename = f"frame_{frame_idx:03d}.jpg"
                frame_path = os.path.join(detection_folder, frame_filename)
                cv2.imwrite(frame_path, annotated_frame)
                
                # Store relative path for web display
                relative_path = f"static/detections/{video_id}/{frame_filename}"
                annotated_frames.append({
                    'path': relative_path,
                    'frame_number': i,
                    'vehicle_count': frame_vehicle_count,
                    'detections': detections_info
                })
                
                vehicle_counts.append(frame_vehicle_count)
                print(f"  Frame {i}: {frame_vehicle_count} vehicles detected")
                
                frame_idx += 1
        
        cap.release()
        
        # Calculate statistics
        avg_vehicles = int(np.mean(vehicle_counts)) if vehicle_counts else 0
        max_vehicles = int(np.max(vehicle_counts)) if vehicle_counts else 0
        min_vehicles = int(np.min(vehicle_counts)) if vehicle_counts else 0
        total_detections = sum(vehicle_counts)
        
        # Determine traffic level
        if avg_vehicles < 5:
            traffic_level = 'Low'
        elif avg_vehicles < 15:
            traffic_level = 'Medium'
        else:
            traffic_level = 'High'
        
        # Calculate frame-by-frame vehicle type distribution
        frame_vehicle_breakdown = []
        for frame_data in annotated_frames:
            frame_breakdown = {'cars': 0, 'motorcycles': 0, 'buses': 0, 'trucks': 0}
            for detection in frame_data['detections']:
                vtype = detection['type']
                if vtype in frame_breakdown:
                    frame_breakdown[vtype] += 1
            frame_vehicle_breakdown.append(frame_breakdown)
        
        # Calculate traffic density over time
        time_intervals = []
        for idx, count in enumerate(vehicle_counts):
            time_intervals.append({
                'frame': idx + 1,
                'count': count,
                'density': 'High' if count > avg_vehicles * 1.5 else ('Medium' if count > avg_vehicles * 0.5 else 'Low')
            })
        
        return {
            'duration': round(duration, 2),
            'fps': fps,
            'resolution': f"{width}x{height}",
            'total_frames': frame_count,
            'analyzed_frames': len(vehicle_counts),
            'average_vehicles': avg_vehicles,
            'peak_vehicles': max_vehicles,
            'minimum_vehicles': min_vehicles,
            'total_detections': total_detections,
            'traffic_level': traffic_level,
            'vehicle_counts': vehicle_counts,
            'vehicle_types': vehicle_types,
            'detection_method': 'YOLOv8',
            'annotated_frames': annotated_frames,
            'frame_vehicle_breakdown': frame_vehicle_breakdown,
            'time_intervals': time_intervals
        }
    except Exception as e:
        print(f"Error analyzing video: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'error': str(e),
            'average_vehicles': 0,
            'traffic_level': 'Unknown'
        }

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(upload_path, filename)

@app.route('/get_uploads')
def get_uploads():
    """Get list of uploaded videos"""
    try:
        files = []
        for filename in os.listdir(upload_path):
            if allowed_file(filename):
                filepath = os.path.join(upload_path, filename)
                file_size = os.path.getsize(filepath)
                files.append({
                    'filename': filename,
                    'size': round(file_size / (1024 * 1024), 2),  # Size in MB
                    'uploaded': datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                })
        return jsonify({
            'success': True,
            'files': sorted(files, key=lambda x: x['uploaded'], reverse=True)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚦 TRAFFIC MONITORING SYSTEM - WEB INTERFACE")
    print("="*70)
    print("\n✅ Server starting...")
    print("📊 Model loaded successfully!")
    print("\n🌐 Open your browser and go to:")
    print("   http://localhost:5000")
    print("\n🛑 Press CTRL+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
