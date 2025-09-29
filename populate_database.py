"""
Database Population Script
Populates the agriculture advisory system database with sample data
"""

from flask_models import *
from datetime import datetime, date, timedelta
import json
import random
import numpy as np

def populate_sample_data():
    """Populate database with comprehensive sample data"""
    print("🌱 Populating Agriculture Advisory System Database...")
    print("=" * 50)

    # 1. Create sample locations
    print("📍 Creating locations...")
    locations_data = [
        {"country": "India", "state": "Punjab", "district": "Ludhiana", "city": "Ludhiana", "pincode": "141001", "latitude": 30.7333, "longitude": 76.7794},
        {"country": "India", "state": "Haryana", "district": "Karnal", "city": "Karnal", "pincode": "132001", "latitude": 29.6857, "longitude": 76.9905},
        {"country": "India", "state": "Uttar Pradesh", "district": "Meerut", "city": "Meerut", "pincode": "250001", "latitude": 28.9845, "longitude": 77.7064},
        {"country": "India", "state": "Maharashtra", "district": "Nashik", "city": "Nashik", "pincode": "422001", "latitude": 19.9975, "longitude": 73.7898},
        {"country": "India", "state": "Karnataka", "district": "Bangalore Rural", "city": "Devanahalli", "pincode": "562110", "latitude": 13.2429, "longitude": 77.7085},
        {"country": "India", "state": "Tamil Nadu", "district": "Coimbatore", "city": "Coimbatore", "pincode": "641001", "latitude": 11.0168, "longitude": 76.9558},
        {"country": "India", "state": "Andhra Pradesh", "district": "Krishna", "city": "Vijayawada", "pincode": "520001", "latitude": 16.5062, "longitude": 80.6480},
        {"country": "India", "state": "Rajasthan", "district": "Jaipur", "city": "Jaipur", "pincode": "302001", "latitude": 26.9124, "longitude": 75.7873}
    ]

    locations = []
    for loc_data in locations_data:
        location = Location(**loc_data)
        db.session.add(location)
        locations.append(location)

    db.session.flush()  # To get IDs
    print(f"✅ Created {len(locations)} locations")

    # 2. Create sample users
    print("👥 Creating users...")
    users_data = [
        {"username": "farmer1", "email": "farmer1@example.com", "first_name": "Rajesh", "last_name": "Kumar", "phone": "9876543210", "user_type": "farmer"},
        {"username": "farmer2", "email": "farmer2@example.com", "first_name": "Priya", "last_name": "Sharma", "phone": "9876543211", "user_type": "farmer"},
        {"username": "farmer3", "email": "farmer3@example.com", "first_name": "Suresh", "last_name": "Patel", "phone": "9876543212", "user_type": "farmer"},
        {"username": "advisor1", "email": "advisor1@example.com", "first_name": "Dr. Amit", "last_name": "Singh", "phone": "9876543213", "user_type": "advisor"},
        {"username": "admin1", "email": "admin@example.com", "first_name": "System", "last_name": "Admin", "phone": "9876543214", "user_type": "admin"}
    ]

    users = []
    for user_data in users_data:
        user = User(**user_data)
        user.set_password("password123")  # Default password
        db.session.add(user)
        users.append(user)

    db.session.flush()
    print(f"✅ Created {len(users)} users")

    # 3. Create sample farms
    print("🚜 Creating farms...")
    farms_data = [
        {"user_id": users[0].id, "farm_name": "Green Valley Farm", "location_id": locations[0].id, "total_area": 25.5, "farm_type": "conventional", "irrigation_type": "drip", "soil_type": "Loamy"},
        {"user_id": users[0].id, "farm_name": "Sunrise Farm", "location_id": locations[1].id, "total_area": 18.2, "farm_type": "organic", "irrigation_type": "sprinkler", "soil_type": "Sandy"},
        {"user_id": users[1].id, "farm_name": "Golden Fields", "location_id": locations[2].id, "total_area": 32.0, "farm_type": "conventional", "irrigation_type": "flood", "soil_type": "Clay"},
        {"user_id": users[1].id, "farm_name": "Eco Farm", "location_id": locations[3].id, "total_area": 15.8, "farm_type": "organic", "irrigation_type": "drip", "soil_type": "Black"},
        {"user_id": users[2].id, "farm_name": "Heritage Farm", "location_id": locations[4].id, "total_area": 28.7, "farm_type": "mixed", "irrigation_type": "rain_fed", "soil_type": "Red"}
    ]

    farms = []
    for farm_data in farms_data:
        farm = Farm(**farm_data)
        db.session.add(farm)
        farms.append(farm)

    db.session.flush()
    print(f"✅ Created {len(farms)} farms")

    # 4. Create soil data for farms
    print("🌍 Creating soil data...")
    for farm in farms:
        soil_data = SoilData(
            farm_id=farm.id,
            nitrogen_content=random.uniform(20, 80),
            phosphorus_content=random.uniform(15, 60),
            potassium_content=random.uniform(25, 70),
            ph_level=random.uniform(6.0, 8.0),
            organic_carbon=random.uniform(0.5, 2.5),
            sulfur_content=random.uniform(10, 40),
            zinc_content=random.uniform(0.5, 3.0),
            iron_content=random.uniform(2.0, 15.0),
            electrical_conductivity=random.uniform(0.2, 1.5),
            moisture_content=random.uniform(15, 35),
            soil_temperature=random.uniform(18, 32),
            test_date=date.today() - timedelta(days=random.randint(1, 90)),
            tested_by="Soil Testing Laboratory",
            lab_name="AgriTest Labs"
        )
        db.session.add(soil_data)

    print(f"✅ Created soil data for {len(farms)} farms")

    # 5. Create crop master data
    print("🌾 Creating crop master data...")
    crops_data = [
        {"crop_name": "Rice", "scientific_name": "Oryza sativa", "crop_category": "cereal", "growing_season": "kharif", "maturity_period": 120, "water_requirement": "high"},
        {"crop_name": "Wheat", "scientific_name": "Triticum aestivum", "crop_category": "cereal", "growing_season": "rabi", "maturity_period": 110, "water_requirement": "medium"},
        {"crop_name": "Maize", "scientific_name": "Zea mays", "crop_category": "cereal", "growing_season": "kharif", "maturity_period": 90, "water_requirement": "medium"},
        {"crop_name": "Cotton", "scientific_name": "Gossypium", "crop_category": "cash_crop", "growing_season": "kharif", "maturity_period": 180, "water_requirement": "high"},
        {"crop_name": "Sugarcane", "scientific_name": "Saccharum officinarum", "crop_category": "cash_crop", "growing_season": "perennial", "maturity_period": 365, "water_requirement": "high"},
        {"crop_name": "Soybean", "scientific_name": "Glycine max", "crop_category": "oilseed", "growing_season": "kharif", "maturity_period": 95, "water_requirement": "medium"},
        {"crop_name": "Chickpea", "scientific_name": "Cicer arietinum", "crop_category": "pulse", "growing_season": "rabi", "maturity_period": 100, "water_requirement": "low"},
        {"crop_name": "Tomato", "scientific_name": "Solanum lycopersicum", "crop_category": "vegetable", "growing_season": "rabi", "maturity_period": 75, "water_requirement": "medium"},
        {"crop_name": "Potato", "scientific_name": "Solanum tuberosum", "crop_category": "vegetable", "growing_season": "rabi", "maturity_period": 90, "water_requirement": "medium"},
        {"crop_name": "Onion", "scientific_name": "Allium cepa", "crop_category": "vegetable", "growing_season": "rabi", "maturity_period": 120, "water_requirement": "medium"}
    ]

    crops = []
    for crop_data in crops_data:
        crop = Crop(**crop_data)
        db.session.add(crop)
        crops.append(crop)

    db.session.flush()
    print(f"✅ Created {len(crops)} crops")

    # 6. Create crop requirements
    print("📋 Creating crop requirements...")
    for crop in crops:
        requirements = CropRequirement(
            crop_id=crop.id,
            min_temperature=random.uniform(15, 25),
            max_temperature=random.uniform(35, 45),
            optimal_temperature=random.uniform(25, 35),
            min_rainfall=random.uniform(400, 600),
            max_rainfall=random.uniform(1200, 2000),
            optimal_rainfall=random.uniform(800, 1200),
            min_humidity=random.uniform(40, 60),
            max_humidity=random.uniform(80, 95),
            optimal_humidity=random.uniform(65, 80),
            min_ph=random.uniform(5.5, 6.5),
            max_ph=random.uniform(7.5, 8.5),
            optimal_ph=random.uniform(6.5, 7.5),
            nitrogen_requirement=random.uniform(40, 120),
            phosphorus_requirement=random.uniform(20, 60),
            potassium_requirement=random.uniform(30, 80),
            water_requirement_per_season=random.uniform(500, 1500),
            sunlight_hours_required=random.uniform(6, 12)
        )
        db.session.add(requirements)

    print(f"✅ Created requirements for {len(crops)} crops")

    # 7. Create fertilizer data
    print("🧪 Creating fertilizer data...")
    fertilizers_data = [
        {"fertilizer_name": "Urea", "fertilizer_type": "inorganic", "nitrogen_content": 46.0, "phosphorus_content": 0.0, "potassium_content": 0.0, "cost_per_kg": 6.50},
        {"fertilizer_name": "DAP", "fertilizer_type": "inorganic", "nitrogen_content": 18.0, "phosphorus_content": 46.0, "potassium_content": 0.0, "cost_per_kg": 27.00},
        {"fertilizer_name": "MOP", "fertilizer_type": "inorganic", "nitrogen_content": 0.0, "phosphorus_content": 0.0, "potassium_content": 60.0, "cost_per_kg": 20.00},
        {"fertilizer_name": "NPK 19:19:19", "fertilizer_type": "inorganic", "nitrogen_content": 19.0, "phosphorus_content": 19.0, "potassium_content": 19.0, "cost_per_kg": 35.00},
        {"fertilizer_name": "Compost", "fertilizer_type": "organic", "nitrogen_content": 1.5, "phosphorus_content": 1.0, "potassium_content": 1.5, "cost_per_kg": 8.00},
        {"fertilizer_name": "Vermicompost", "fertilizer_type": "organic", "nitrogen_content": 2.0, "phosphorus_content": 1.5, "potassium_content": 1.8, "cost_per_kg": 12.00}
    ]

    fertilizers = []
    for fert_data in fertilizers_data:
        fertilizer = Fertilizer(**fert_data)
        db.session.add(fertilizer)
        fertilizers.append(fertilizer)

    db.session.flush()
    print(f"✅ Created {len(fertilizers)} fertilizers")

    # 8. Create pesticide data
    print("🦠 Creating pesticide data...")
    pesticides_data = [
        {"pesticide_name": "Chlorpyrifos", "pesticide_type": "insecticide", "active_ingredient": "Chlorpyrifos", "concentration": 20.0, "toxicity_level": "medium", "cost_per_liter": 450.00},
        {"pesticide_name": "Mancozeb", "pesticide_type": "fungicide", "active_ingredient": "Mancozeb", "concentration": 75.0, "toxicity_level": "low", "cost_per_liter": 320.00},
        {"pesticide_name": "2,4-D", "pesticide_type": "herbicide", "active_ingredient": "2,4-Dichlorophenoxyacetic acid", "concentration": 38.0, "toxicity_level": "medium", "cost_per_liter": 280.00},
        {"pesticide_name": "Neem Oil", "pesticide_type": "insecticide", "active_ingredient": "Azadirachtin", "concentration": 1.0, "toxicity_level": "low", "cost_per_liter": 180.00}
    ]

    pesticides = []
    for pest_data in pesticides_data:
        pesticide = Pesticide(**pest_data)
        db.session.add(pesticide)
        pesticides.append(pesticide)

    db.session.flush()
    print(f"✅ Created {len(pesticides)} pesticides")

    # 9. Create disease/pest data
    print("🐛 Creating disease/pest data...")
    diseases_data = [
        {"name": "Late Blight", "type": "disease", "scientific_name": "Phytophthora infestans", "symptoms": "Brown spots on leaves, white mold on undersides", "severity_level": "high"},
        {"name": "Aphids", "type": "pest", "scientific_name": "Aphidoidea", "symptoms": "Small green insects on leaves and stems", "severity_level": "medium"},
        {"name": "Blast", "type": "disease", "scientific_name": "Magnaporthe oryzae", "symptoms": "Diamond-shaped lesions on leaves", "severity_level": "high"},
        {"name": "Stem Borer", "type": "pest", "scientific_name": "Chilo suppressalis", "symptoms": "Dead hearts, white ears in rice", "severity_level": "high"}
    ]

    diseases = []
    for disease_data in diseases_data:
        disease = CropDiseasePest(**disease_data)
        db.session.add(disease)
        diseases.append(disease)

    db.session.flush()
    print(f"✅ Created {len(diseases)} diseases/pests")

    # 10. Create weather data
    print("🌤️ Creating weather data...")
    for location in locations:
        for i in range(30):  # Last 30 days
            weather_date = date.today() - timedelta(days=i)
            weather = WeatherData(
                location_id=location.id,
                date=weather_date,
                temperature_max=random.uniform(25, 40),
                temperature_min=random.uniform(15, 25),
                temperature_avg=random.uniform(20, 32),
                humidity=random.uniform(40, 90),
                rainfall=random.uniform(0, 50) if random.random() < 0.3 else 0,
                wind_speed=random.uniform(5, 25),
                pressure=random.uniform(1000, 1020),
                cloud_cover=random.uniform(0, 100)
            )
            db.session.add(weather)

    print(f"✅ Created weather data for {len(locations)} locations")

    # 11. Create market prices
    print("💰 Creating market prices...")
    for crop in crops[:5]:  # Top 5 crops
        for location in locations[:3]:  # Top 3 locations
            for i in range(7):  # Last 7 days
                price_date = date.today() - timedelta(days=i)
                base_price = random.uniform(2000, 8000)
                market_price = MarketPrice(
                    crop_id=crop.id,
                    location_id=location.id,
                    price_per_quintal=base_price + random.uniform(-500, 500),
                    date=price_date,
                    market_name=f"{location.city} Mandi",
                    market_type="wholesale"
                )
                db.session.add(market_price)

    print("✅ Created market price data")

    # 12. Create sample recommendations
    print("💡 Creating sample recommendations...")
    farmer_users = [u for u in users if u.user_type == 'farmer']

    for user in farmer_users:
        user_farms = [f for f in farms if f.user_id == user.id]

        for farm in user_farms:
            # Crop recommendation
            crop_rec = CropRecommendation(
                user_id=user.id,
                farm_id=farm.id,
                recommended_crops=json.dumps([
                    {"crop": "Rice", "confidence": 0.85, "expected_yield": "45 quintals/acre"},
                    {"crop": "Wheat", "confidence": 0.78, "expected_yield": "42 quintals/acre"}
                ]),
                input_parameters=json.dumps({
                    "nitrogen": 65, "phosphorus": 45, "potassium": 55,
                    "temperature": 28, "humidity": 70, "ph": 6.8, "rainfall": 800
                }),
                season="kharif",
                year=2024,
                confidence_score=0.85
            )
            db.session.add(crop_rec)

            # Fertilizer recommendation
            fert_rec = FertilizerRecommendation(
                user_id=user.id,
                farm_id=farm.id,
                crop_id=crops[0].id,
                recommended_fertilizers=json.dumps([
                    {"name": "Urea", "quantity": "50 kg/acre", "cost": 325},
                    {"name": "DAP", "quantity": "25 kg/acre", "cost": 675}
                ]),
                soil_test_data=json.dumps({
                    "nitrogen": 45, "phosphorus": 30, "potassium": 40, "ph": 6.5
                }),
                estimated_cost=1000
            )
            db.session.add(fert_rec)

    print("✅ Created sample recommendations")

    # 13. Create notifications
    print("🔔 Creating notifications...")
    for user in farmer_users:
        notifications_data = [
            {"user_id": user.id, "notification_type": "weather_alert", "title": "Heavy Rain Alert", "message": "Heavy rainfall expected in next 24 hours. Take necessary precautions.", "priority": "high"},
            {"user_id": user.id, "notification_type": "crop_advisory", "title": "Crop Advisory", "message": "This is the best time for sowing wheat in your region.", "priority": "medium"},
            {"user_id": user.id, "notification_type": "market_price", "title": "Price Update", "message": "Rice prices have increased by 5% in your local market.", "priority": "low"}
        ]

        for notif_data in notifications_data:
            notification = Notification(**notif_data)
            db.session.add(notification)

    print("✅ Created notifications")

    # 14. Create knowledge base articles
    print("📚 Creating knowledge base articles...")
    kb_articles = [
        {
            "title": "Best Practices for Rice Cultivation",
            "content": "Rice cultivation requires proper water management, timely sowing, and appropriate fertilizer application...",
            "category": "crop_cultivation",
            "tags": json.dumps(["rice", "cultivation", "water management"]),
            "difficulty_level": "beginner"
        },
        {
            "title": "Integrated Pest Management in Cotton",
            "content": "IPM approach combines biological, cultural, and chemical methods for effective pest control...",
            "category": "pest_control", 
            "tags": json.dumps(["cotton", "IPM", "pest control"]),
            "difficulty_level": "intermediate"
        },
        {
            "title": "Soil Health Management",
            "content": "Maintaining soil health through organic matter addition, proper pH management, and nutrient balance...",
            "category": "soil_management",
            "tags": json.dumps(["soil health", "organic matter", "pH"]),
            "difficulty_level": "intermediate"
        }
    ]

    for article_data in kb_articles:
        article = KnowledgeBase(**article_data)
        db.session.add(article)

    print("✅ Created knowledge base articles")

    # Commit all changes
    try:
        db.session.commit()
        print("\n" + "=" * 50)
        print("🎉 DATABASE POPULATION COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("📊 Summary:")
        print(f"   • {len(locations)} Locations")
        print(f"   • {len(users)} Users") 
        print(f"   • {len(farms)} Farms")
        print(f"   • {len(crops)} Crops")
        print(f"   • {len(fertilizers)} Fertilizers")
        print(f"   • {len(pesticides)} Pesticides")
        print(f"   • {len(diseases)} Diseases/Pests")
        print(f"   • Weather data for 30 days")
        print(f"   • Market prices for major crops")
        print(f"   • Sample recommendations")
        print(f"   • User notifications")
        print(f"   • Knowledge base articles")
        print("\n✅ Your agriculture advisory system is now ready to use!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error during database population: {str(e)}")
        raise

if __name__ == "__main__":
    # This would be run within Flask app context
    print("⚠️ This script should be run within Flask application context")
    print("Usage: flask shell -> exec(open('populate_database.py').read())")
