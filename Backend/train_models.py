"""
Machine Learning Model Training Scripts
For Agriculture Advisory System

This script trains models for:
1. Crop Recommendation
2. Fertilizer Recommendation  
3. Disease Detection (using images)
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import warnings
warnings.filterwarnings('ignore')

class CropRecommendationModel:
    """Crop Recommendation Model using Random Forest"""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def prepare_data(self, csv_file_path=None):
        """Prepare crop recommendation dataset"""
        if csv_file_path:
            # Load actual dataset
            df = pd.read_csv(csv_file_path)
        else:
            # Create sample data based on common crop recommendation parameters
            np.random.seed(42)
            n_samples = 2200

            # Sample data generation (replace with actual dataset)
            data = {
                'N': np.random.uniform(0, 140, n_samples),
                'P': np.random.uniform(5, 145, n_samples),
                'K': np.random.uniform(5, 205, n_samples),
                'temperature': np.random.uniform(8.8, 43.7, n_samples),
                'humidity': np.random.uniform(14, 100, n_samples),
                'ph': np.random.uniform(3.5, 9.9, n_samples),
                'rainfall': np.random.uniform(20, 300, n_samples)
            }

            # Sample crop labels
            crops = ['rice', 'wheat', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
                    'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
                    'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
                    'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee']

            labels = np.random.choice(crops, n_samples)
            data['label'] = labels

            df = pd.DataFrame(data)

        return df

    def train(self, csv_file_path=None):
        """Train the crop recommendation model"""
        print("🌱 Training Crop Recommendation Model...")

        # Prepare data
        df = self.prepare_data(csv_file_path)

        # Features and target
        X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
        y = df['label']

        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"✅ Crop Recommendation Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, 
                                  target_names=self.label_encoder.classes_))

        return accuracy

    def predict(self, input_data):
        """Make crop recommendations"""
        input_scaled = self.scaler.transform(input_data)
        prediction = self.model.predict(input_scaled)
        probabilities = self.model.predict_proba(input_scaled)

        # Get top 3 recommendations
        top_indices = np.argsort(probabilities[0])[-3:][::-1]
        recommendations = []

        for idx in top_indices:
            crop_name = self.label_encoder.inverse_transform([idx])[0]
            confidence = probabilities[0][idx]
            recommendations.append({
                'crop': crop_name,
                'confidence': confidence
            })

        return recommendations

    def save_model(self, model_path='models/crop_recommendation_model.pkl'):
        """Save the trained model"""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder
        }
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"✅ Model saved to {model_path}")

class FertilizerRecommendationModel:
    """Fertilizer Recommendation Model"""

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()

    def prepare_data(self):
        """Prepare fertilizer recommendation dataset"""
        np.random.seed(42)
        n_samples = 1000

        # Sample fertilizer recommendation data
        data = {
            'Temparature': np.random.uniform(15, 40, n_samples),
            'Humidity': np.random.uniform(20, 90, n_samples),
            'Moisture': np.random.uniform(10, 80, n_samples),
            'Soil Type': np.random.choice(['Sandy', 'Loamy', 'Black', 'Red', 'Clayey'], n_samples),
            'Crop Type': np.random.choice(['Wheat', 'Rice', 'Maize', 'Cotton', 'Sugarcane'], n_samples),
            'Nitrogen': np.random.uniform(0, 50, n_samples),
            'Potassium': np.random.uniform(0, 50, n_samples),
            'Phosphorous': np.random.uniform(0, 50, n_samples)
        }

        # Fertilizer types based on NPK requirements
        fertilizers = ['10-26-26', '14-35-14', '17-17-17', '20-20', '28-28', 'DAP', 'Urea']
        data['Fertilizer Name'] = np.random.choice(fertilizers, n_samples)

        return pd.DataFrame(data)

    def train(self):
        """Train fertilizer recommendation model"""
        print("🧪 Training Fertilizer Recommendation Model...")

        df = self.prepare_data()

        # Encode categorical variables
        df_encoded = df.copy()
        df_encoded['Soil Type'] = LabelEncoder().fit_transform(df['Soil Type'])
        df_encoded['Crop Type'] = LabelEncoder().fit_transform(df['Crop Type'])

        # Features and target
        X = df_encoded[['Temparature', 'Humidity', 'Moisture', 'Soil Type', 
                       'Crop Type', 'Nitrogen', 'Potassium', 'Phosphorous']]
        y = df_encoded['Fertilizer Name']

        # Encode target
        y_encoded = self.label_encoder.fit_transform(y)

        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )

        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train
        self.model.fit(X_train_scaled, y_train)

        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"✅ Fertilizer Recommendation Model Accuracy: {accuracy:.4f}")

        return accuracy

    def save_model(self, model_path='models/fertilizer_recommendation_model.pkl'):
        """Save the trained model"""
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder
        }
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"✅ Model saved to {model_path}")

class DiseaseDetectionModel:
    """Disease Detection Model using CNN"""

    def __init__(self):
        self.model = None
        self.input_shape = (224, 224, 3)
        self.num_classes = 38  # Based on PlantVillage dataset

    def build_model(self):
        """Build CNN model for disease detection"""
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            MaxPooling2D(2, 2),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(2, 2),
            Flatten(),
            Dropout(0.5),
            Dense(512, activation='relu'),
            Dense(self.num_classes, activation='softmax')
        ])

        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def train(self, data_dir=None):
        """Train disease detection model"""
        print("🦠 Training Disease Detection Model...")

        if data_dir and os.path.exists(data_dir):
            # Use actual dataset if available
            datagen = ImageDataGenerator(
                rescale=1./255,
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                horizontal_flip=True,
                validation_split=0.2
            )

            train_generator = datagen.flow_from_directory(
                data_dir,
                target_size=(224, 224),
                batch_size=32,
                class_mode='categorical',
                subset='training'
            )

            validation_generator = datagen.flow_from_directory(
                data_dir,
                target_size=(224, 224),
                batch_size=32,
                class_mode='categorical',
                subset='validation'
            )

            self.model = self.build_model()

            history = self.model.fit(
                train_generator,
                steps_per_epoch=len(train_generator),
                epochs=10,
                validation_data=validation_generator,
                validation_steps=len(validation_generator)
            )

            return history
        else:
            print("⚠️ No dataset directory provided. Skipping disease detection model training.")
            return None

    def save_model(self, model_path='models/disease_detection_model.h5'):
        """Save the trained model"""
        if self.model:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            self.model.save(model_path)
            print(f"✅ Model saved to {model_path}")

def create_sample_datasets():
    """Create sample datasets for testing"""
    print("📊 Creating sample datasets...")

    # Create crop recommendation dataset
    crop_model = CropRecommendationModel()
    crop_df = crop_model.prepare_data()
    crop_df.to_csv('datasets/crop_recommendation.csv', index=False)
    print("✅ Crop recommendation dataset created")

    # Create fertilizer recommendation dataset
    fert_model = FertilizerRecommendationModel()
    fert_df = fert_model.prepare_data()
    fert_df.to_csv('datasets/fertilizer_recommendation.csv', index=False)
    print("✅ Fertilizer recommendation dataset created")

    print("📁 Sample datasets saved in datasets/ folder")

def train_all_models():
    """Train all ML models"""
    print("🚀 Starting ML Model Training Pipeline...")
    print("=" * 50)

    # Create directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('datasets', exist_ok=True)

    # Create sample datasets
    create_sample_datasets()

    # Train Crop Recommendation Model
    print("\n1. CROP RECOMMENDATION MODEL")
    print("-" * 30)
    crop_model = CropRecommendationModel()
    crop_accuracy = crop_model.train('datasets/crop_recommendation.csv')
    crop_model.save_model()

    # Train Fertilizer Recommendation Model
    print("\n2. FERTILIZER RECOMMENDATION MODEL")
    print("-" * 35)
    fert_model = FertilizerRecommendationModel()
    fert_accuracy = fert_model.train()
    fert_model.save_model()

    # Train Disease Detection Model (if dataset available)
    print("\n3. DISEASE DETECTION MODEL")
    print("-" * 25)
    disease_model = DiseaseDetectionModel()
    disease_model.train()  # This will skip if no dataset

    print("\n" + "=" * 50)
    print("🎉 MODEL TRAINING COMPLETED!")
    print(f"📈 Crop Recommendation Accuracy: {crop_accuracy:.4f}")
    print(f"📈 Fertilizer Recommendation Accuracy: {fert_accuracy:.4f}")
    print("📁 Models saved in models/ folder")
    print("📊 Datasets saved in datasets/ folder")

if __name__ == "__main__":
    train_all_models()
