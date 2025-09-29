"""
Flask SQLAlchemy Models for Agriculture Advisory System
Created for: Crop Advisory System with AI/ML Integration
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Decimal, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

# User Management Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    user_type = db.Column(db.Enum('farmer', 'advisor', 'admin', name='user_type'), default='farmer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farms = relationship("Farm", back_populates="user", cascade="all, delete-orphan")
    crop_recommendations = relationship("CropRecommendation", back_populates="user")
    fertilizer_recommendations = relationship("FertilizerRecommendation", back_populates="user")
    pesticide_recommendations = relationship("PesticideRecommendation", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    preferences = relationship("UserPreference", back_populates="user", uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# Location Model
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50))
    pincode = db.Column(db.String(10))
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    farms = relationship("Farm", back_populates="location")
    weather_data = relationship("WeatherData", back_populates="location")
    market_prices = relationship("MarketPrice", back_populates="location")
    notifications = relationship("Notification", back_populates="location")

# Farm Model
class Farm(db.Model):
    __tablename__ = 'farms'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_name = db.Column(db.String(100), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    total_area = db.Column(db.Numeric(10, 2), nullable=False)  # in acres
    farm_type = db.Column(db.Enum('organic', 'conventional', 'mixed', name='farm_type'), default='conventional')
    irrigation_type = db.Column(db.Enum('drip', 'sprinkler', 'flood', 'rain_fed', 'mixed', name='irrigation_type'))
    soil_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="farms")
    location = relationship("Location", back_populates="farms")
    soil_data = relationship("SoilData", back_populates="farm", cascade="all, delete-orphan")
    crop_recommendations = relationship("CropRecommendation", back_populates="farm")
    fertilizer_recommendations = relationship("FertilizerRecommendation", back_populates="farm")
    pesticide_recommendations = relationship("PesticideRecommendation", back_populates="farm")
    farm_activities = relationship("FarmActivity", back_populates="farm")
    yield_records = relationship("YieldRecord", back_populates="farm")

# Soil Data Model
class SoilData(db.Model):
    __tablename__ = 'soil_data'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    nitrogen_content = db.Column(db.Numeric(5, 2), nullable=False)
    phosphorus_content = db.Column(db.Numeric(5, 2), nullable=False)
    potassium_content = db.Column(db.Numeric(5, 2), nullable=False)
    ph_level = db.Column(db.Numeric(3, 1), nullable=False)
    organic_carbon = db.Column(db.Numeric(5, 2))
    sulfur_content = db.Column(db.Numeric(5, 2))
    zinc_content = db.Column(db.Numeric(5, 2))
    iron_content = db.Column(db.Numeric(5, 2))
    manganese_content = db.Column(db.Numeric(5, 2))
    copper_content = db.Column(db.Numeric(5, 2))
    boron_content = db.Column(db.Numeric(5, 2))
    electrical_conductivity = db.Column(db.Numeric(5, 2))
    moisture_content = db.Column(db.Numeric(5, 2))
    soil_temperature = db.Column(db.Numeric(5, 2))
    test_date = db.Column(db.Date, nullable=False)
    tested_by = db.Column(db.String(100))
    lab_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    farm = relationship("Farm", back_populates="soil_data")

# Weather Data Model
class WeatherData(db.Model):
    __tablename__ = 'weather_data'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    temperature_max = db.Column(db.Numeric(5, 2))
    temperature_min = db.Column(db.Numeric(5, 2))
    temperature_avg = db.Column(db.Numeric(5, 2))
    humidity = db.Column(db.Numeric(5, 2))
    rainfall = db.Column(db.Numeric(7, 2))  # in mm
    wind_speed = db.Column(db.Numeric(5, 2))
    wind_direction = db.Column(db.String(10))
    solar_radiation = db.Column(db.Numeric(8, 2))
    evapotranspiration = db.Column(db.Numeric(6, 2))
    pressure = db.Column(db.Numeric(7, 2))
    cloud_cover = db.Column(db.Numeric(5, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    location = relationship("Location", back_populates="weather_data")

    __table_args__ = (db.UniqueConstraint('location_id', 'date', name='unique_location_date'),)

# Crop Master Data Model
class Crop(db.Model):
    __tablename__ = 'crops'

    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), unique=True, nullable=False)
    scientific_name = db.Column(db.String(100))
    crop_category = db.Column(db.Enum('cereal', 'pulse', 'oilseed', 'vegetable', 'fruit', 'cash_crop', 'fodder', 'spice', name='crop_category'), nullable=False)
    growing_season = db.Column(db.Enum('kharif', 'rabi', 'zaid', 'perennial', name='growing_season'), nullable=False)
    maturity_period = db.Column(db.Integer)  # in days
    water_requirement = db.Column(db.Enum('low', 'medium', 'high', name='water_requirement'), default='medium')
    soil_type_preference = db.Column(db.Text)  # JSON array
    climate_requirement = db.Column(db.Text)  # JSON object
    nutritional_info = db.Column(db.Text)  # JSON object
    market_demand = db.Column(db.Enum('low', 'medium', 'high', name='market_demand'), default='medium')
    profit_margin = db.Column(db.Enum('low', 'medium', 'high', name='profit_margin'), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    requirements = relationship("CropRequirement", back_populates="crop", uselist=False)
    market_prices = relationship("MarketPrice", back_populates="crop")
    fertilizer_recommendations = relationship("FertilizerRecommendation", back_populates="crop")
    pesticide_recommendations = relationship("PesticideRecommendation", back_populates="crop")
    farm_activities = relationship("FarmActivity", back_populates="crop")
    yield_records = relationship("YieldRecord", back_populates="crop")

    def get_soil_preferences(self):
        return json.loads(self.soil_type_preference) if self.soil_type_preference else []

    def get_climate_requirements(self):
        return json.loads(self.climate_requirement) if self.climate_requirement else {}

# Crop Requirements Model
class CropRequirement(db.Model):
    __tablename__ = 'crop_requirements'

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    min_temperature = db.Column(db.Numeric(5, 2))
    max_temperature = db.Column(db.Numeric(5, 2))
    optimal_temperature = db.Column(db.Numeric(5, 2))
    min_rainfall = db.Column(db.Numeric(7, 2))
    max_rainfall = db.Column(db.Numeric(7, 2))
    optimal_rainfall = db.Column(db.Numeric(7, 2))
    min_humidity = db.Column(db.Numeric(5, 2))
    max_humidity = db.Column(db.Numeric(5, 2))
    optimal_humidity = db.Column(db.Numeric(5, 2))
    min_ph = db.Column(db.Numeric(3, 1))
    max_ph = db.Column(db.Numeric(3, 1))
    optimal_ph = db.Column(db.Numeric(3, 1))
    nitrogen_requirement = db.Column(db.Numeric(5, 2))
    phosphorus_requirement = db.Column(db.Numeric(5, 2))
    potassium_requirement = db.Column(db.Numeric(5, 2))
    water_requirement_per_season = db.Column(db.Numeric(8, 2))  # in mm
    sunlight_hours_required = db.Column(db.Numeric(4, 1))

    # Relationships
    crop = relationship("Crop", back_populates="requirements")

# Fertilizer Model
class Fertilizer(db.Model):
    __tablename__ = 'fertilizers'

    id = db.Column(db.Integer, primary_key=True)
    fertilizer_name = db.Column(db.String(100), unique=True, nullable=False)
    fertilizer_type = db.Column(db.Enum('organic', 'inorganic', 'bio_fertilizer', name='fertilizer_type'), nullable=False)
    nitrogen_content = db.Column(db.Numeric(5, 2), default=0)
    phosphorus_content = db.Column(db.Numeric(5, 2), default=0)
    potassium_content = db.Column(db.Numeric(5, 2), default=0)
    sulfur_content = db.Column(db.Numeric(5, 2), default=0)
    calcium_content = db.Column(db.Numeric(5, 2), default=0)
    magnesium_content = db.Column(db.Numeric(5, 2), default=0)
    micronutrients = db.Column(db.Text)  # JSON object
    application_method = db.Column(db.Enum('soil_application', 'foliar_spray', 'fertigation', 'seed_treatment', name='application_method'))
    recommended_dosage_per_acre = db.Column(db.Text)  # JSON object
    cost_per_kg = db.Column(db.Numeric(8, 2))
    availability_status = db.Column(db.Enum('available', 'limited', 'out_of_stock', name='availability_status'), default='available')
    manufacturer = db.Column(db.String(100))
    safety_precautions = db.Column(db.Text)
    storage_instructions = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Pesticide Model
class Pesticide(db.Model):
    __tablename__ = 'pesticides'

    id = db.Column(db.Integer, primary_key=True)
    pesticide_name = db.Column(db.String(100), unique=True, nullable=False)
    pesticide_type = db.Column(db.Enum('insecticide', 'fungicide', 'herbicide', 'bactericide', 'nematicide', name='pesticide_type'), nullable=False)
    active_ingredient = db.Column(db.String(100), nullable=False)
    concentration = db.Column(db.Numeric(5, 2))
    target_pests = db.Column(db.Text)  # JSON array
    suitable_crops = db.Column(db.Text)  # JSON array
    application_method = db.Column(db.Enum('spray', 'dusting', 'soil_treatment', 'seed_treatment', 'fumigation', name='application_method'))
    recommended_dosage = db.Column(db.Text)  # JSON object
    pre_harvest_interval = db.Column(db.Integer)  # days
    re_entry_interval = db.Column(db.Integer)  # hours
    toxicity_level = db.Column(db.Enum('low', 'medium', 'high', name='toxicity_level'), default='medium')
    environmental_impact = db.Column(db.Enum('low', 'medium', 'high', name='environmental_impact'), default='medium')
    cost_per_liter = db.Column(db.Numeric(8, 2))
    manufacturer = db.Column(db.String(100))
    registration_number = db.Column(db.String(50))
    safety_precautions = db.Column(db.Text)
    first_aid_measures = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Crop Diseases and Pests Model
class CropDiseasePest(db.Model):
    __tablename__ = 'crop_diseases_pests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('disease', 'pest', 'weed', name='disease_pest_type'), nullable=False)
    scientific_name = db.Column(db.String(100))
    affected_crops = db.Column(db.Text)  # JSON array
    symptoms = db.Column(db.Text)
    causes = db.Column(db.Text)
    favorable_conditions = db.Column(db.Text)  # JSON object
    prevention_methods = db.Column(db.Text)
    organic_control_methods = db.Column(db.Text)
    chemical_control_methods = db.Column(db.Text)
    severity_level = db.Column(db.Enum('low', 'medium', 'high', 'critical', name='severity_level'), default='medium')
    economic_importance = db.Column(db.Enum('minor', 'moderate', 'major', 'critical', name='economic_importance'), default='moderate')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    pesticide_recommendations = relationship("PesticideRecommendation", back_populates="disease_pest")

# Market Price Model
class MarketPrice(db.Model):
    __tablename__ = 'market_prices'

    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    market_name = db.Column(db.String(100))
    price_per_quintal = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False)
    quality_grade = db.Column(db.Enum('A', 'B', 'C', 'FAQ', name='quality_grade'), default='FAQ')
    market_type = db.Column(db.Enum('wholesale', 'retail', 'government', 'online', name='market_type'), default='wholesale')
    demand_level = db.Column(db.Enum('low', 'medium', 'high', name='demand_level'), default='medium')
    supply_level = db.Column(db.Enum('low', 'medium', 'high', name='supply_level'), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    crop = relationship("Crop", back_populates="market_prices")
    location = relationship("Location", back_populates="market_prices")

# Crop Recommendation Model
class CropRecommendation(db.Model):
    __tablename__ = 'crop_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    recommended_crops = db.Column(db.Text, nullable=False)  # JSON array
    input_parameters = db.Column(db.Text, nullable=False)  # JSON object
    model_version = db.Column(db.String(20))
    confidence_score = db.Column(db.Numeric(5, 4))
    season = db.Column(db.Enum('kharif', 'rabi', 'zaid', name='season'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    implementation_status = db.Column(db.Enum('pending', 'implemented', 'rejected', name='implementation_status'), default='pending')
    actual_yield = db.Column(db.Numeric(10, 2))
    feedback_rating = db.Column(db.Integer)
    feedback_comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="crop_recommendations")
    farm = relationship("Farm", back_populates="crop_recommendations")

    def get_recommended_crops(self):
        return json.loads(self.recommended_crops) if self.recommended_crops else []

    def get_input_parameters(self):
        return json.loads(self.input_parameters) if self.input_parameters else {}

# Fertilizer Recommendation Model
class FertilizerRecommendation(db.Model):
    __tablename__ = 'fertilizer_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    recommended_fertilizers = db.Column(db.Text, nullable=False)  # JSON array
    soil_test_data = db.Column(db.Text, nullable=False)  # JSON object
    application_schedule = db.Column(db.Text)  # JSON object
    estimated_cost = db.Column(db.Numeric(10, 2))
    expected_yield_increase = db.Column(db.Numeric(5, 2))  # percentage
    environmental_impact_score = db.Column(db.Numeric(3, 2))
    implementation_status = db.Column(db.Enum('pending', 'implemented', 'rejected', name='implementation_status'), default='pending')
    actual_results = db.Column(db.Text)  # JSON object
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="fertilizer_recommendations")
    farm = relationship("Farm", back_populates="fertilizer_recommendations")
    crop = relationship("Crop", back_populates="fertilizer_recommendations")

# Pesticide Recommendation Model
class PesticideRecommendation(db.Model):
    __tablename__ = 'pesticide_recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    disease_pest_id = db.Column(db.Integer, db.ForeignKey('crop_diseases_pests.id'))
    recommended_pesticides = db.Column(db.Text, nullable=False)  # JSON array
    problem_description = db.Column(db.Text, nullable=False)
    severity_assessment = db.Column(db.Enum('low', 'medium', 'high', 'critical', name='severity_assessment'), nullable=False)
    treatment_priority = db.Column(db.Enum('immediate', 'within_week', 'routine', name='treatment_priority'), default='routine')
    application_instructions = db.Column(db.Text)
    estimated_cost = db.Column(db.Numeric(8, 2))
    safety_recommendations = db.Column(db.Text)
    alternative_methods = db.Column(db.Text)
    implementation_status = db.Column(db.Enum('pending', 'implemented', 'rejected', name='implementation_status'), default='pending')
    effectiveness_rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="pesticide_recommendations")
    farm = relationship("Farm", back_populates="pesticide_recommendations")
    crop = relationship("Crop", back_populates="pesticide_recommendations")
    disease_pest = relationship("CropDiseasePest", back_populates="pesticide_recommendations")

# Notification Model
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.Enum('weather_alert', 'disease_outbreak', 'market_price', 'crop_advisory', 'fertilizer_reminder', 'harvest_reminder', name='notification_type'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('low', 'medium', 'high', 'critical', name='priority'), default='medium')
    is_read = db.Column(db.Boolean, default=False)
    action_required = db.Column(db.Boolean, default=False)
    expiry_date = db.Column(db.Date)
    location_specific = db.Column(db.Boolean, default=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")
    location = relationship("Location", back_populates="notifications")

# Farm Activity Model
class FarmActivity(db.Model):
    __tablename__ = 'farm_activities'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'))
    activity_type = db.Column(db.Enum('sowing', 'irrigation', 'fertilizer_application', 'pesticide_spray', 'weeding', 'harvesting', 'soil_testing', 'other', name='activity_type'), nullable=False)
    activity_description = db.Column(db.Text, nullable=False)
    activity_date = db.Column(db.Date, nullable=False)
    area_covered = db.Column(db.Numeric(8, 2))  # in acres
    inputs_used = db.Column(db.Text)  # JSON object
    cost_incurred = db.Column(db.Numeric(10, 2))
    labor_hours = db.Column(db.Numeric(6, 2))
    weather_conditions = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    farm = relationship("Farm", back_populates="farm_activities")
    crop = relationship("Crop", back_populates="farm_activities")

# Yield Record Model
class YieldRecord(db.Model):
    __tablename__ = 'yield_records'

    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    harvest_date = db.Column(db.Date, nullable=False)
    area_harvested = db.Column(db.Numeric(8, 2), nullable=False)  # in acres
    total_yield = db.Column(db.Numeric(10, 2), nullable=False)  # in quintals
    yield_per_acre = db.Column(db.Numeric(8, 2), nullable=False)  # in quintals per acre
    quality_grade = db.Column(db.Enum('A', 'B', 'C', 'FAQ', name='quality_grade'), default='FAQ')
    moisture_content = db.Column(db.Numeric(5, 2))
    total_cost = db.Column(db.Numeric(12, 2))  # total cultivation cost
    selling_price_per_quintal = db.Column(db.Numeric(8, 2))
    total_revenue = db.Column(db.Numeric(12, 2))
    net_profit = db.Column(db.Numeric(12, 2))
    profit_per_acre = db.Column(db.Numeric(10, 2))
    season = db.Column(db.Enum('kharif', 'rabi', 'zaid', name='season'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    farm = relationship("Farm", back_populates="yield_records")
    crop = relationship("Crop", back_populates="yield_records")

# Knowledge Base Model
class KnowledgeBase(db.Model):
    __tablename__ = 'knowledge_base'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.Enum('crop_cultivation', 'soil_management', 'pest_control', 'irrigation', 'post_harvest', 'market_information', 'government_schemes', name='kb_category'), nullable=False)
    tags = db.Column(db.Text)  # JSON array
    author = db.Column(db.String(100))
    difficulty_level = db.Column(db.Enum('beginner', 'intermediate', 'advanced', name='difficulty_level'), default='beginner')
    language = db.Column(db.String(10), default='en')
    views_count = db.Column(db.Integer, default=0)
    likes_count = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    published_date = db.Column(db.Date)
    updated_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# User Preferences Model
class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    preferred_language = db.Column(db.String(10), default='en')
    preferred_units = db.Column(db.Enum('metric', 'imperial', name='preferred_units'), default='metric')
    notification_preferences = db.Column(db.Text)  # JSON object
    privacy_settings = db.Column(db.Text)  # JSON object
    dashboard_layout = db.Column(db.Text)  # JSON object
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="preferences")
