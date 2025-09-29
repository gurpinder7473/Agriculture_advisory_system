
-- Comprehensive Agriculture Advisory System Database Schema

-- User Management Tables
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(15),
    user_type ENUM('farmer', 'advisor', 'admin') DEFAULT 'farmer',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Location/Geographic Data
CREATE TABLE locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    district VARCHAR(50) NOT NULL,
    city VARCHAR(50),
    pincode VARCHAR(10),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Farm Information
CREATE TABLE farms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_name VARCHAR(100) NOT NULL,
    location_id INTEGER NOT NULL,
    total_area DECIMAL(10, 2) NOT NULL, -- in acres
    farm_type ENUM('organic', 'conventional', 'mixed') DEFAULT 'conventional',
    irrigation_type ENUM('drip', 'sprinkler', 'flood', 'rain_fed', 'mixed'),
    soil_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Soil Data
CREATE TABLE soil_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    nitrogen_content DECIMAL(5, 2) NOT NULL, -- N content in soil
    phosphorus_content DECIMAL(5, 2) NOT NULL, -- P content in soil
    potassium_content DECIMAL(5, 2) NOT NULL, -- K content in soil
    ph_level DECIMAL(3, 1) NOT NULL,
    organic_carbon DECIMAL(5, 2),
    sulfur_content DECIMAL(5, 2),
    zinc_content DECIMAL(5, 2),
    iron_content DECIMAL(5, 2),
    manganese_content DECIMAL(5, 2),
    copper_content DECIMAL(5, 2),
    boron_content DECIMAL(5, 2),
    electrical_conductivity DECIMAL(5, 2), -- EC in dS/m
    moisture_content DECIMAL(5, 2),
    soil_temperature DECIMAL(5, 2),
    test_date DATE NOT NULL,
    tested_by VARCHAR(100),
    lab_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id) ON DELETE CASCADE
);

-- Weather Data
CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    date DATE NOT NULL,
    temperature_max DECIMAL(5, 2),
    temperature_min DECIMAL(5, 2),
    temperature_avg DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    rainfall DECIMAL(7, 2), -- in mm
    wind_speed DECIMAL(5, 2),
    wind_direction VARCHAR(10),
    solar_radiation DECIMAL(8, 2),
    evapotranspiration DECIMAL(6, 2),
    pressure DECIMAL(7, 2),
    cloud_cover DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (location_id) REFERENCES locations(id),
    UNIQUE KEY unique_location_date (location_id, date)
);

-- Crop Master Data
CREATE TABLE crops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name VARCHAR(100) NOT NULL UNIQUE,
    scientific_name VARCHAR(100),
    crop_category ENUM('cereal', 'pulse', 'oilseed', 'vegetable', 'fruit', 'cash_crop', 'fodder', 'spice') NOT NULL,
    growing_season ENUM('kharif', 'rabi', 'zaid', 'perennial') NOT NULL,
    maturity_period INTEGER, -- in days
    water_requirement ENUM('low', 'medium', 'high') DEFAULT 'medium',
    soil_type_preference TEXT, -- JSON array of suitable soil types
    climate_requirement TEXT, -- JSON object with climate preferences
    nutritional_info TEXT, -- JSON object with nutritional information
    market_demand ENUM('low', 'medium', 'high') DEFAULT 'medium',
    profit_margin ENUM('low', 'medium', 'high') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crop Growing Requirements
CREATE TABLE crop_requirements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_id INTEGER NOT NULL,
    min_temperature DECIMAL(5, 2),
    max_temperature DECIMAL(5, 2),
    optimal_temperature DECIMAL(5, 2),
    min_rainfall DECIMAL(7, 2),
    max_rainfall DECIMAL(7, 2),
    optimal_rainfall DECIMAL(7, 2),
    min_humidity DECIMAL(5, 2),
    max_humidity DECIMAL(5, 2),
    optimal_humidity DECIMAL(5, 2),
    min_ph DECIMAL(3, 1),
    max_ph DECIMAL(3, 1),
    optimal_ph DECIMAL(3, 1),
    nitrogen_requirement DECIMAL(5, 2),
    phosphorus_requirement DECIMAL(5, 2),
    potassium_requirement DECIMAL(5, 2),
    water_requirement_per_season DECIMAL(8, 2), -- in mm
    sunlight_hours_required DECIMAL(4, 1),
    FOREIGN KEY (crop_id) REFERENCES crops(id) ON DELETE CASCADE
);

-- Fertilizer Master Data
CREATE TABLE fertilizers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fertilizer_name VARCHAR(100) NOT NULL UNIQUE,
    fertilizer_type ENUM('organic', 'inorganic', 'bio_fertilizer') NOT NULL,
    nitrogen_content DECIMAL(5, 2) DEFAULT 0,
    phosphorus_content DECIMAL(5, 2) DEFAULT 0,
    potassium_content DECIMAL(5, 2) DEFAULT 0,
    sulfur_content DECIMAL(5, 2) DEFAULT 0,
    calcium_content DECIMAL(5, 2) DEFAULT 0,
    magnesium_content DECIMAL(5, 2) DEFAULT 0,
    micronutrients TEXT, -- JSON object for micronutrients
    application_method ENUM('soil_application', 'foliar_spray', 'fertigation', 'seed_treatment'),
    recommended_dosage_per_acre TEXT, -- JSON object with crop-specific dosages
    cost_per_kg DECIMAL(8, 2),
    availability_status ENUM('available', 'limited', 'out_of_stock') DEFAULT 'available',
    manufacturer VARCHAR(100),
    safety_precautions TEXT,
    storage_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pesticide/Disease Management Data
CREATE TABLE pesticides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pesticide_name VARCHAR(100) NOT NULL UNIQUE,
    pesticide_type ENUM('insecticide', 'fungicide', 'herbicide', 'bactericide', 'nematicide') NOT NULL,
    active_ingredient VARCHAR(100) NOT NULL,
    concentration DECIMAL(5, 2),
    target_pests TEXT, -- JSON array of target pests/diseases
    suitable_crops TEXT, -- JSON array of suitable crops
    application_method ENUM('spray', 'dusting', 'soil_treatment', 'seed_treatment', 'fumigation'),
    recommended_dosage TEXT, -- JSON object with crop and pest specific dosages
    pre_harvest_interval INTEGER, -- days before harvest
    re_entry_interval INTEGER, -- hours before re-entry
    toxicity_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    environmental_impact ENUM('low', 'medium', 'high') DEFAULT 'medium',
    cost_per_liter DECIMAL(8, 2),
    manufacturer VARCHAR(100),
    registration_number VARCHAR(50),
    safety_precautions TEXT,
    first_aid_measures TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crop Diseases and Pests
CREATE TABLE crop_diseases_pests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type ENUM('disease', 'pest', 'weed') NOT NULL,
    scientific_name VARCHAR(100),
    affected_crops TEXT, -- JSON array of affected crops
    symptoms TEXT,
    causes TEXT,
    favorable_conditions TEXT, -- JSON object with environmental conditions
    prevention_methods TEXT,
    organic_control_methods TEXT,
    chemical_control_methods TEXT,
    severity_level ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    economic_importance ENUM('minor', 'moderate', 'major', 'critical') DEFAULT 'moderate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market Price Data
CREATE TABLE market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    market_name VARCHAR(100),
    price_per_quintal DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    quality_grade ENUM('A', 'B', 'C', 'FAQ') DEFAULT 'FAQ',
    market_type ENUM('wholesale', 'retail', 'government', 'online') DEFAULT 'wholesale',
    demand_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    supply_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (crop_id) REFERENCES crops(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Crop Recommendations History
CREATE TABLE crop_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    recommended_crops TEXT NOT NULL, -- JSON array of recommended crops with scores
    input_parameters TEXT NOT NULL, -- JSON object with all input parameters
    model_version VARCHAR(20),
    confidence_score DECIMAL(5, 4),
    season ENUM('kharif', 'rabi', 'zaid') NOT NULL,
    year INTEGER NOT NULL,
    implementation_status ENUM('pending', 'implemented', 'rejected') DEFAULT 'pending',
    actual_yield DECIMAL(10, 2), -- actual yield if implemented
    feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5),
    feedback_comments TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (farm_id) REFERENCES farms(id)
);

-- Fertilizer Recommendations History
CREATE TABLE fertilizer_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    recommended_fertilizers TEXT NOT NULL, -- JSON array of fertilizer recommendations
    soil_test_data TEXT NOT NULL, -- JSON object with soil test results
    application_schedule TEXT, -- JSON object with timing and quantities
    estimated_cost DECIMAL(10, 2),
    expected_yield_increase DECIMAL(5, 2), -- percentage increase
    environmental_impact_score DECIMAL(3, 2),
    implementation_status ENUM('pending', 'implemented', 'rejected') DEFAULT 'pending',
    actual_results TEXT, -- JSON object with actual results if implemented
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (farm_id) REFERENCES farms(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
);

-- Pesticide Recommendations History
CREATE TABLE pesticide_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    farm_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    disease_pest_id INTEGER,
    recommended_pesticides TEXT NOT NULL, -- JSON array of pesticide recommendations
    problem_description TEXT NOT NULL,
    severity_assessment ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    treatment_priority ENUM('immediate', 'within_week', 'routine') DEFAULT 'routine',
    application_instructions TEXT,
    estimated_cost DECIMAL(8, 2),
    safety_recommendations TEXT,
    alternative_methods TEXT, -- organic/biological alternatives
    implementation_status ENUM('pending', 'implemented', 'rejected') DEFAULT 'pending',
    effectiveness_rating INTEGER CHECK (effectiveness_rating >= 1 AND effectiveness_rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (farm_id) REFERENCES farms(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id),
    FOREIGN KEY (disease_pest_id) REFERENCES crop_diseases_pests(id)
);

-- Notifications and Alerts
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_type ENUM('weather_alert', 'disease_outbreak', 'market_price', 'crop_advisory', 'fertilizer_reminder', 'harvest_reminder') NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    is_read BOOLEAN DEFAULT FALSE,
    action_required BOOLEAN DEFAULT FALSE,
    expiry_date DATE,
    location_specific BOOLEAN DEFAULT FALSE,
    location_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

-- Farm Activities Log
CREATE TABLE farm_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    crop_id INTEGER,
    activity_type ENUM('sowing', 'irrigation', 'fertilizer_application', 'pesticide_spray', 'weeding', 'harvesting', 'soil_testing', 'other') NOT NULL,
    activity_description TEXT NOT NULL,
    activity_date DATE NOT NULL,
    area_covered DECIMAL(8, 2), -- in acres
    inputs_used TEXT, -- JSON object with inputs like fertilizers, pesticides, seeds
    cost_incurred DECIMAL(10, 2),
    labor_hours DECIMAL(6, 2),
    weather_conditions TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
);

-- Yield Records
CREATE TABLE yield_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER NOT NULL,
    crop_id INTEGER NOT NULL,
    harvest_date DATE NOT NULL,
    area_harvested DECIMAL(8, 2) NOT NULL, -- in acres
    total_yield DECIMAL(10, 2) NOT NULL, -- in quintals
    yield_per_acre DECIMAL(8, 2) NOT NULL, -- in quintals per acre
    quality_grade ENUM('A', 'B', 'C', 'FAQ') DEFAULT 'FAQ',
    moisture_content DECIMAL(5, 2),
    total_cost DECIMAL(12, 2), -- total cultivation cost
    selling_price_per_quintal DECIMAL(8, 2),
    total_revenue DECIMAL(12, 2),
    net_profit DECIMAL(12, 2),
    profit_per_acre DECIMAL(10, 2),
    season ENUM('kharif', 'rabi', 'zaid') NOT NULL,
    year INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (farm_id) REFERENCES farms(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
);

-- Knowledge Base Articles
CREATE TABLE knowledge_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category ENUM('crop_cultivation', 'soil_management', 'pest_control', 'irrigation', 'post_harvest', 'market_information', 'government_schemes') NOT NULL,
    tags TEXT, -- JSON array of tags
    author VARCHAR(100),
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    language VARCHAR(10) DEFAULT 'en',
    views_count INTEGER DEFAULT 0,
    likes_count INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    published_date DATE,
    updated_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Preferences and Settings
CREATE TABLE user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    preferred_language VARCHAR(10) DEFAULT 'en',
    preferred_units ENUM('metric', 'imperial') DEFAULT 'metric',
    notification_preferences TEXT, -- JSON object with notification settings
    privacy_settings TEXT, -- JSON object with privacy settings
    dashboard_layout TEXT, -- JSON object with dashboard preferences
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_farms_user_id ON farms(user_id);
CREATE INDEX idx_soil_data_farm_id ON soil_data(farm_id);
CREATE INDEX idx_weather_data_location_date ON weather_data(location_id, date);
CREATE INDEX idx_market_prices_crop_location_date ON market_prices(crop_id, location_id, date);
CREATE INDEX idx_crop_recommendations_user_farm ON crop_recommendations(user_id, farm_id);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);
CREATE INDEX idx_farm_activities_farm_date ON farm_activities(farm_id, activity_date);
CREATE INDEX idx_yield_records_farm_year_season ON yield_records(farm_id, year, season);
