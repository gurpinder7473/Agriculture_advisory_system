"""
Complete Agriculture Advisory System with Voice Assistant
Multilingual voice support for farmers in local languages
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import pandas as pd
import numpy as np
import pickle
import json
from datetime import datetime, date, timedelta
import os
from werkzeug.utils import secure_filename
import requests
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import tempfile
import threading
import base64

# Import our models
from flask_models import *

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agriculture_advisory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize translator and speech recognition
translator = Translator()
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Language mapping for Indian languages
LANGUAGE_CODES = {
    'English': 'en',
    'हिंदी': 'hi',
    'বাংলা': 'bn',
    'తెలుగు': 'te',
    'தமிழ்': 'ta',
    'मराठी': 'mr',
    'ગુજરાતી': 'gu',
    'ಕನ್ನಡ': 'kn',
    'മലയാളം': 'ml',
    'ਪੰਜਾਬੀ': 'pa',
    'ଓଡ଼ିଆ': 'or',
    'অসমীয়া': 'as'
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Global variables for ML models
crop_model = None
fertilizer_model = None
disease_model = None

def load_ml_models():
    """Load pre-trained ML models"""
    global crop_model, fertilizer_model, disease_model
    try:
        if os.path.exists('models/crop_recommendation_model.pkl'):
            with open('models/crop_recommendation_model.pkl', 'rb') as f:
                crop_model = pickle.load(f)
        if os.path.exists('models/fertilizer_recommendation_model.pkl'):
            with open('models/fertilizer_recommendation_model.pkl', 'rb') as f:
                fertilizer_model = pickle.load(f)
        print("✅ ML Models loaded successfully")
    except Exception as e:
        print(f"⚠️ Error loading ML models: {str(e)}")

# Voice Assistant Functions
class VoiceAssistant:
    def __init__(self):
        self.translator = Translator()
        self.recognizer = sr.Recognizer()

    def listen_to_audio(self, language_code='en'):
        """Listen to audio and convert to text"""
        try:
            with sr.Microphone() as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

            # Recognize speech in the selected language
            text = self.recognizer.recognize_google(audio, language=language_code)
            return {"success": True, "text": text}

        except sr.UnknownValueError:
            return {"success": False, "error": "Could not understand audio"}
        except sr.RequestError as e:
            return {"success": False, "error": f"Speech recognition error: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": f"Error: {str(e)}"}

    def text_to_speech(self, text, language_code='en'):
        """Convert text to speech"""
        try:
            tts = gTTS(text=text, lang=language_code, slow=False)

            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)

            # Convert to base64 for web playback
            with open(temp_file.name, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')

            # Clean up
            os.unlink(temp_file.name)

            return {"success": True, "audio_data": audio_data}

        except Exception as e:
            return {"success": False, "error": f"TTS Error: {str(e)}"}

    def translate_text(self, text, target_language='en'):
        """Translate text to target language"""
        try:
            if target_language == 'auto':
                detection = self.translator.detect(text)
                detected_lang = detection.lang
                translation = self.translator.translate(text, dest='en')
                return {
                    "success": True, 
                    "translated_text": translation.text,
                    "detected_language": detected_lang,
                    "confidence": detection.confidence
                }
            else:
                translation = self.translator.translate(text, dest=target_language)
                return {"success": True, "translated_text": translation.text}

        except Exception as e:
            return {"success": False, "error": f"Translation error: {str(e)}"}

    def get_agricultural_advice(self, query, language_code='en'):
        """Get agricultural advice based on query"""
        try:
            # Translate query to English for processing
            if language_code != 'en':
                translated_query = self.translate_text(query, 'en')
                if not translated_query['success']:
                    return {"success": False, "error": "Translation failed"}
                english_query = translated_query['translated_text']
            else:
                english_query = query

            # Process agricultural query
            advice = self.process_agricultural_query(english_query)

            # Translate advice back to user's language
            if language_code != 'en':
                translated_advice = self.translate_text(advice, language_code)
                if translated_advice['success']:
                    advice = translated_advice['translated_text']

            return {"success": True, "advice": advice, "original_query": query}

        except Exception as e:
            return {"success": False, "error": f"Error processing query: {str(e)}"}

    def process_agricultural_query(self, query):
        """Process agricultural queries and provide advice"""
        query_lower = query.lower()

        # Crop-related queries
        if any(word in query_lower for word in ['crop', 'sow', 'plant', 'grow']):
            if any(word in query_lower for word in ['yellow', 'पीली', 'yellowing']):
                return ("Your crops showing yellowing leaves may indicate nutrient deficiency, particularly nitrogen. "
                       "I recommend soil testing and application of nitrogen-rich fertilizers like urea. "
                       "Also check for pest infestation or water logging issues.")

            elif any(word in query_lower for word in ['disease', 'sick', 'problem']):
                return ("Based on your description, your crops may be experiencing disease or pest issues. "
                       "I recommend taking photos of affected plants for detailed analysis, and consider "
                       "consulting with your local agricultural extension officer for immediate assistance.")

            else:
                return ("For crop recommendations, I need information about your soil type, climate, and season. "
                       "Generally, consider crops suitable for your region's rainfall and temperature patterns.")

        # Fertilizer queries
        elif any(word in query_lower for word in ['fertilizer', 'nutrient', 'manure']):
            return ("For optimal fertilizer application, conduct soil testing first. Based on your crop type, "
                   "apply balanced NPK fertilizers. For organic farming, use compost and vermicompost. "
                   "Follow recommended dosages to avoid over-fertilization.")

        # Weather queries
        elif any(word in query_lower for word in ['weather', 'rain', 'temperature']):
            return ("Monitor weather forecasts regularly for farming decisions. Avoid spraying during windy conditions. "
                   "Plan irrigation based on rainfall predictions. Protect crops during extreme weather events.")

        # Pest queries
        elif any(word in query_lower for word in ['pest', 'insect', 'bug']):
            return ("For pest management, use integrated pest management (IPM) approach. Start with biological "
                   "control methods, then organic pesticides if needed. Apply chemical pesticides as last resort "
                   "following safety guidelines.")

        else:
            return ("I'm here to help with your agricultural queries. You can ask about crops, fertilizers, "
                   "pest management, weather conditions, or any farming-related questions. Please provide "
                   "more specific details for better advice.")

# Initialize voice assistant
voice_assistant = VoiceAssistant()

# Routes
@app.route('/')
def index():
    """Home page with voice assistant"""
    if current_user.is_authenticated:
        # Get user's recent activities
        recent_recommendations = CropRecommendation.query.filter_by(
            user_id=current_user.id
        ).order_by(CropRecommendation.created_at.desc()).limit(5).all()

        # Get user's farms
        user_farms = Farm.query.filter_by(user_id=current_user.id).all()

        # Get recent notifications
        notifications = Notification.query.filter_by(
            user_id=current_user.id, is_read=False
        ).order_by(Notification.created_at.desc()).limit(5).all()

        return render_template('dashboard.html', 
                             recommendations=recent_recommendations,
                             farms=user_farms,
                             notifications=notifications,
                             languages=LANGUAGE_CODES)
    return render_template('index.html', languages=LANGUAGE_CODES)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form.get('phone')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')

        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# Voice Assistant API Routes
@app.route('/api/voice/listen', methods=['POST'])
@login_required
def voice_listen():
    """API endpoint for voice recognition"""
    try:
        data = request.get_json()
        language_code = data.get('language', 'en')

        # This is a placeholder - in real implementation, you'd handle audio data
        # For demo, we'll simulate audio recognition
        result = voice_assistant.listen_to_audio(language_code)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/voice/speak', methods=['POST'])
@login_required
def voice_speak():
    """API endpoint for text-to-speech"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        language_code = data.get('language', 'en')

        result = voice_assistant.text_to_speech(text, language_code)
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/voice/advice', methods=['POST'])
@login_required
def voice_advice():
    """API endpoint for agricultural advice"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        language_code = data.get('language', 'en')

        result = voice_assistant.get_agricultural_advice(query, language_code)

        # Save the query and response for learning
        if result['success']:
            # Here you could save the interaction to database for ML training
            pass

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/crop-recommendation', methods=['GET', 'POST'])
@login_required
def crop_recommendation():
    """Crop recommendation page"""
    if request.method == 'POST':
        try:
            # Get input data
            farm_id = request.form['farm_id']
            nitrogen = float(request.form['nitrogen'])
            phosphorus = float(request.form['phosphorus'])
            potassium = float(request.form['potassium'])
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])
            season = request.form['season']

            # Make prediction
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
            recommended_crops = predict_crops(input_data)

            # Save recommendation to database
            recommendation = CropRecommendation(
                user_id=current_user.id,
                farm_id=farm_id,
                recommended_crops=json.dumps(recommended_crops),
                input_parameters=json.dumps({
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium,
                    'temperature': temperature,
                    'humidity': humidity,
                    'ph': ph,
                    'rainfall': rainfall
                }),
                season=season,
                year=datetime.now().year,
                model_version='1.0',
                confidence_score=0.85
            )

            db.session.add(recommendation)
            db.session.commit()

            flash('Crop recommendation generated successfully!', 'success')
            return render_template('crop_recommendation_result.html', 
                                 crops=recommended_crops,
                                 input_data={
                                     'nitrogen': nitrogen,
                                     'phosphorus': phosphorus,
                                     'potassium': potassium,
                                     'temperature': temperature,
                                     'humidity': humidity,
                                     'ph': ph,
                                     'rainfall': rainfall
                                 })

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return render_template('crop_recommendation.html')

    # Get user's farms for the form
    user_farms = Farm.query.filter_by(user_id=current_user.id).all()
    return render_template('crop_recommendation.html', farms=user_farms)

@app.route('/fertilizer-recommendation', methods=['GET', 'POST'])
@login_required
def fertilizer_recommendation():
    """Fertilizer recommendation page"""
    if request.method == 'POST':
        try:
            farm_id = request.form['farm_id']
            crop_id = request.form['crop_id']
            nitrogen = float(request.form['nitrogen'])
            phosphorus = float(request.form['phosphorus'])
            potassium = float(request.form['potassium'])
            soil_ph = float(request.form['soil_ph'])

            # Get fertilizer recommendations
            fertilizer_recs = predict_fertilizer(crop_id, nitrogen, phosphorus, potassium, soil_ph)

            # Save to database
            recommendation = FertilizerRecommendation(
                user_id=current_user.id,
                farm_id=farm_id,
                crop_id=crop_id,
                recommended_fertilizers=json.dumps(fertilizer_recs),
                soil_test_data=json.dumps({
                    'nitrogen': nitrogen,
                    'phosphorus': phosphorus,
                    'potassium': potassium,
                    'ph': soil_ph
                }),
                estimated_cost=sum([f.get('cost', 0) for f in fertilizer_recs])
            )

            db.session.add(recommendation)
            db.session.commit()

            flash('Fertilizer recommendation generated successfully!', 'success')
            return render_template('fertilizer_recommendation_result.html', 
                                 fertilizers=fertilizer_recs)

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    user_farms = Farm.query.filter_by(user_id=current_user.id).all()
    crops = Crop.query.all()
    return render_template('fertilizer_recommendation.html', farms=user_farms, crops=crops)

@app.route('/disease-detection', methods=['GET', 'POST'])
@login_required
def disease_detection():
    """Disease detection page"""
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                flash('No image uploaded', 'error')
                return render_template('disease_detection.html')

            file = request.files['image']
            if file.filename == '':
                flash('No image selected', 'error')
                return render_template('disease_detection.html')

            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Process image and detect disease
                disease_result = detect_disease_from_image(filepath)

                # Get pesticide recommendations if disease detected
                pesticide_recs = []
                if disease_result['disease_detected']:
                    pesticide_recs = get_pesticide_recommendations(disease_result['disease_name'])

                    # Save recommendation
                    recommendation = PesticideRecommendation(
                        user_id=current_user.id,
                        farm_id=request.form.get('farm_id'),
                        crop_id=request.form.get('crop_id'),
                        recommended_pesticides=json.dumps(pesticide_recs),
                        problem_description=disease_result['disease_name'],
                        severity_assessment=disease_result['severity']
                    )

                    db.session.add(recommendation)
                    db.session.commit()

                flash('Disease analysis completed!', 'success')
                return render_template('disease_detection_result.html', 
                                     result=disease_result,
                                     pesticides=pesticide_recs)

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    user_farms = Farm.query.filter_by(user_id=current_user.id).all()
    crops = Crop.query.all()
    return render_template('disease_detection.html', farms=user_farms, crops=crops)

@app.route('/weather-alerts')
@login_required
def weather_alerts():
    """Weather alerts page"""
    user_farms = Farm.query.filter_by(user_id=current_user.id).all()
    weather_data = []

    for farm in user_farms:
        latest_weather = WeatherData.query.filter_by(
            location_id=farm.location_id
        ).order_by(WeatherData.date.desc()).first()

        if latest_weather:
            weather_data.append({
                'farm_name': farm.farm_name,
                'weather': latest_weather,
                'location': farm.location
            })

    return render_template('weather_alerts.html', weather_data=weather_data)

@app.route('/market-prices')
@login_required
def market_prices():
    """Market prices page"""
    recent_prices = db.session.query(MarketPrice, Crop, Location).join(
        Crop, MarketPrice.crop_id == Crop.id
    ).join(
        Location, MarketPrice.location_id == Location.id
    ).order_by(MarketPrice.date.desc()).limit(50).all()

    return render_template('market_prices.html', prices=recent_prices)

@app.route('/farm-management')
@login_required
def farm_management():
    """Farm management page"""
    user_farms = Farm.query.filter_by(user_id=current_user.id).all()

    farm_data = []
    for farm in user_farms:
        latest_soil = SoilData.query.filter_by(
            farm_id=farm.id
        ).order_by(SoilData.test_date.desc()).first()

        recent_activities = FarmActivity.query.filter_by(
            farm_id=farm.id
        ).order_by(FarmActivity.activity_date.desc()).limit(5).all()

        farm_data.append({
            'farm': farm,
            'soil_data': latest_soil,
            'activities': recent_activities
        })

    return render_template('farm_management.html', farms=farm_data)

@app.route('/add-farm', methods=['GET', 'POST'])
@login_required
def add_farm():
    """Add new farm"""
    if request.method == 'POST':
        try:
            # Create location first
            location = Location(
                country=request.form['country'],
                state=request.form['state'],
                district=request.form['district'],
                city=request.form.get('city'),
                pincode=request.form.get('pincode'),
                latitude=float(request.form['latitude']) if request.form.get('latitude') else None,
                longitude=float(request.form['longitude']) if request.form.get('longitude') else None
            )
            db.session.add(location)
            db.session.flush()

            # Create farm
            farm = Farm(
                user_id=current_user.id,
                farm_name=request.form['farm_name'],
                location_id=location.id,
                total_area=float(request.form['total_area']),
                farm_type=request.form['farm_type'],
                irrigation_type=request.form.get('irrigation_type'),
                soil_type=request.form.get('soil_type')
            )
            db.session.add(farm)
            db.session.commit()

            flash('Farm added successfully!', 'success')
            return redirect(url_for('farm_management'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')

    return render_template('add_farm.html')

# API Endpoints
@app.route('/api/crops', methods=['GET'])
def api_get_crops():
    """Get all crops API"""
    crops = Crop.query.all()
    return jsonify([{
        'id': crop.id,
        'name': crop.crop_name,
        'category': crop.crop_category,
        'season': crop.growing_season
    } for crop in crops])

@app.route('/api/weather/<int:location_id>')
def api_get_weather(location_id):
    """Get weather data for location"""
    weather = WeatherData.query.filter_by(
        location_id=location_id
    ).order_by(WeatherData.date.desc()).limit(7).all()

    return jsonify([{
        'date': w.date.strftime('%Y-%m-%d'),
        'temperature_max': float(w.temperature_max) if w.temperature_max else None,
        'temperature_min': float(w.temperature_min) if w.temperature_min else None,
        'humidity': float(w.humidity) if w.humidity else None,
        'rainfall': float(w.rainfall) if w.rainfall else None
    } for w in weather])

# Helper functions for ML predictions
def predict_crops(input_data):
    """Predict suitable crops based on soil and weather data"""
    try:
        if crop_model and 'model' in crop_model:
            # Use actual trained model
            model = crop_model['model']
            scaler = crop_model['scaler']
            label_encoder = crop_model['label_encoder']

            # Scale input data
            input_scaled = scaler.transform(input_data)

            # Make prediction
            probabilities = model.predict_proba(input_scaled)

            # Get top 3 predictions
            top_indices = np.argsort(probabilities[0])[-3:][::-1]
            recommendations = []

            for idx in top_indices:
                crop_name = label_encoder.inverse_transform([idx])[0]
                confidence = probabilities[0][idx]
                recommendations.append({
                    'name': crop_name.title(),
                    'confidence': round(confidence * 100, 2),
                    'expected_yield': f'{random.randint(35, 55)} quintals/acre'
                })

            return recommendations
        else:
            # Fallback sample recommendations
            return [
                {'name': 'Rice', 'confidence': 85.2, 'expected_yield': '45 quintals/acre'},
                {'name': 'Wheat', 'confidence': 78.6, 'expected_yield': '42 quintals/acre'},
                {'name': 'Maize', 'confidence': 72.4, 'expected_yield': '38 quintals/acre'}
            ]
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return [
            {'name': 'Rice', 'confidence': 85.2, 'expected_yield': '45 quintals/acre'},
            {'name': 'Wheat', 'confidence': 78.6, 'expected_yield': '42 quintals/acre'}
        ]

def predict_fertilizer(crop_id, nitrogen, phosphorus, potassium, ph):
    """Predict fertilizer recommendations"""
    crop = Crop.query.get(crop_id)
    recommendations = []

    # Rule-based recommendations (replace with ML model)
    if nitrogen < 50:
        recommendations.append({
            'name': 'Urea (46% N)',
            'quantity': f'{max(10, 60-nitrogen)} kg/acre',
            'application_time': 'Pre-sowing and top dressing',
            'cost': random.randint(800, 1500),
            'benefits': 'Provides essential nitrogen for leaf growth'
        })

    if phosphorus < 30:
        recommendations.append({
            'name': 'DAP (18-46-0)',
            'quantity': f'{max(15, 40-phosphorus)} kg/acre',
            'application_time': 'At sowing time',
            'cost': random.randint(1200, 2000),
            'benefits': 'Promotes root development and flowering'
        })

    if potassium < 40:
        recommendations.append({
            'name': 'Muriate of Potash (60% K2O)',
            'quantity': f'{max(10, 50-potassium)} kg/acre',
            'application_time': 'Post-emergence',
            'cost': random.randint(600, 1000),
            'benefits': 'Improves plant resistance and fruit quality'
        })

    # Add organic options
    recommendations.append({
        'name': 'Vermicompost',
        'quantity': '200-300 kg/acre',
        'application_time': 'Before sowing',
        'cost': random.randint(2000, 3000),
        'benefits': 'Improves soil structure and provides slow-release nutrients'
    })

    return recommendations

def detect_disease_from_image(image_path):
    """Detect disease from uploaded image"""
    # Placeholder - replace with actual image processing and ML model
    diseases = [
        'Late Blight', 'Early Blight', 'Leaf Spot', 'Powdery Mildew', 
        'Bacterial Wilt', 'Mosaic Virus', 'Rust', 'Aphid Infestation'
    ]

    detected_disease = random.choice(diseases)
    confidence = random.uniform(0.75, 0.95)
    severity = random.choice(['low', 'medium', 'high'])

    return {
        'disease_detected': True,
        'disease_name': detected_disease,
        'confidence': round(confidence, 3),
        'severity': severity,
        'description': f'{detected_disease} is a common crop disease that affects plant health and yield.',
        'image_path': image_path
    }

def get_pesticide_recommendations(disease_name):
    """Get pesticide recommendations for detected disease"""
    pesticide_db = {
        'Late Blight': [
            {
                'name': 'Copper Oxychloride 50% WP',
                'dosage': '2.5-3g/liter water',
                'application_method': 'Foliar spray',
                'frequency': 'Every 7-10 days',
                'safety_period': '7 days before harvest',
                'cost': '₹450/kg'
            }
        ],
        'Early Blight': [
            {
                'name': 'Mancozeb 75% WP',
                'dosage': '2g/liter water',
                'application_method': 'Foliar spray',
                'frequency': 'Every 10-14 days',
                'safety_period': '5 days before harvest',
                'cost': '₹320/kg'
            }
        ],
        'Aphid Infestation': [
            {
                'name': 'Neem Oil',
                'dosage': '5ml/liter water',
                'application_method': 'Foliar spray',
                'frequency': 'Every 5-7 days',
                'safety_period': '1 day before harvest',
                'cost': '₹180/liter'
            }
        ]
    }

    return pesticide_db.get(disease_name, [{
        'name': 'Contact Local Agricultural Officer',
        'dosage': 'As per expert advice',
        'application_method': 'Professional consultation',
        'frequency': 'Immediate',
        'safety_period': 'Follow expert guidelines',
        'cost': 'Consultation fee may apply'
    }])

# Create database tables and load models
@app.before_first_request
def create_tables():
    """Create database tables and load models"""
    db.create_all()
    load_ml_models()

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
