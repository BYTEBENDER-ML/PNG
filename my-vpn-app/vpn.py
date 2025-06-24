import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import json
from datetime import datetime, timedelta
import random
from geopy.distance import geodesic
import warnings
warnings.filterwarnings('ignore')

class VPNAnomalyDetector:
    def __init__(self):
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.user_profiles = {}
        self.location_coords = {
            'New York, USA': (40.7128, -74.0060),
            'London, UK': (51.5074, -0.1278),
            'Tokyo, Japan': (35.6762, 139.6503),
            'Sydney, Australia': (-33.8688, 151.2093),
            'Moscow, Russia': (55.7558, 37.6176),
            'Beijing, China': (39.9042, 116.4074),
            'Mumbai, India': (19.0760, 72.8777),
            'São Paulo, Brazil': (-23.5505, -46.6333),
            'Lagos, Nigeria': (6.5244, 3.3792),
            'Unknown Location': (0, 0),
            'Berlin, Germany': (52.5200, 13.4050),
            'Paris, France': (48.8566, 2.3522),
            'Toronto, Canada': (43.6532, -79.3832),
            'Singapore': (1.3521, 103.8198),
            'Dubai, UAE': (25.2048, 55.2708)
        }
        
    def generate_synthetic_data(self, n_samples=10000):
        """Generate synthetic VPN login data for training"""
        
        # Define user archetypes
        user_types = {
            'business_traveler': {
                'base_locations': ['New York, USA', 'London, UK', 'Tokyo, Japan'],
                'travel_frequency': 0.3,
                'devices': ['Desktop', 'Mobile'],
                'login_times': ['business_hours']
            },
            'remote_worker': {
                'base_locations': ['Berlin, Germany', 'Toronto, Canada'],
                'travel_frequency': 0.1,
                'devices': ['Desktop'],
                'login_times': ['business_hours', 'evening']
            },
            'digital_nomad': {
                'base_locations': ['Singapore', 'Dubai, UAE', 'São Paulo, Brazil'],
                'travel_frequency': 0.6,
                'devices': ['Mobile', 'Tablet'],
                'login_times': ['varied']
            },
            'regular_user': {
                'base_locations': ['Mumbai, India', 'Lagos, Nigeria'],
                'travel_frequency': 0.05,
                'devices': ['Mobile'],
                'login_times': ['evening']
            }
        }
        
        data = []
        
        for i in range(n_samples):
            # Create user
            user_id = f"user_{i % 500:03d}"  # 500 unique users
            user_type = random.choice(list(user_types.keys()))
            profile = user_types[user_type]
            
            # Generate timestamp
            base_time = datetime.now() - timedelta(days=random.randint(1, 90))
            timestamp = base_time + timedelta(
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Determine if this is a travel login
            is_traveling = random.random() < profile['travel_frequency']
            
            if is_traveling:
                # Random location (potentially anomalous)
                location = random.choice(list(self.location_coords.keys()))
            else:
                # Base location
                location = random.choice(profile['base_locations'])
            
            # Device and other features
            device = random.choice(profile['devices'])
            session_duration = random.randint(10, 480)  # 10 minutes to 8 hours
            data_transferred = random.randint(50, 5000)  # MB
            
            # Calculate features
            row = {
                'user_id': user_id,
                'timestamp': timestamp,
                'location': location,
                'device_type': device,
                'session_duration': session_duration,
                'data_transferred': data_transferred,
                'hour_of_day': timestamp.hour,
                'day_of_week': timestamp.weekday(),
                'user_type': user_type
            }
            
            data.append(row)
        
        df = pd.DataFrame(data)
        
        # Create anomalies (5-10% of data)
        anomaly_indices = random.sample(range(len(df)), int(len(df) * 0.07))
        df['is_anomaly'] = 0
        df.loc[anomaly_indices, 'is_anomaly'] = 1
        
        # Make anomalies more extreme
        for idx in anomaly_indices:
            if random.random() < 0.5:  # Location anomaly
                df.loc[idx, 'location'] = 'Unknown Location'
            if random.random() < 0.3:  # Time anomaly
                df.loc[idx, 'hour_of_day'] = random.choice([2, 3, 4, 5])  # Very early hours
            if random.random() < 0.4:  # Session anomaly
                df.loc[idx, 'session_duration'] = random.randint(1, 5)  # Very short sessions
        
        return df
    
    def create_user_profiles(self, df):
        """Create user behavior profiles from historical data"""
        profiles = {}
        
        for user_id in df['user_id'].unique():
            user_data = df[df['user_id'] == user_id]
            
            profiles[user_id] = {
                'typical_locations': user_data['location'].value_counts().head(3).index.tolist(),
                'typical_devices': user_data['device_type'].value_counts().head(2).index.tolist(),
                'avg_session_duration': user_data['session_duration'].mean(),
                'typical_hours': user_data.groupby('hour_of_day').size().sort_values(ascending=False).head(5).index.tolist(),
                'login_frequency': len(user_data),
                'locations_visited': user_data['location'].nunique()
            }
        
        self.user_profiles = profiles
        return profiles
    
    def engineer_features(self, df):
        """Engineer features for ML model"""
        df = df.copy()
        
        # Time-based features
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_night'] = df['hour_of_day'].isin([22, 23, 0, 1, 2, 3, 4, 5]).astype(int)
        df['is_business_hours'] = df['hour_of_day'].isin(range(9, 17)).astype(int)
        
        # Location-based features
        df['location_entropy'] = df.groupby('user_id')['location'].transform(lambda x: len(x.unique()))
        
        # User behavior features
        user_stats = df.groupby('user_id').agg({
            'session_duration': ['mean', 'std'],
            'data_transferred': ['mean', 'std'],
            'location': 'nunique'
        }).fillna(0)
        
        user_stats.columns = ['_'.join(col).strip() for col in user_stats.columns.values]
        df = df.join(user_stats, on='user_id')

        # Encode categorical features
        categorical_cols = ['location', 'device_type', 'user_id']
        for col in categorical_cols:
            if col not in self.label_encoders:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
            else:
                df[col] = self.label_encoders[col].transform(df[col])

        # Select final features
        feature_cols = [
            'location', 'device_type', 'session_duration', 'data_transferred',
            'hour_of_day', 'day_of_week', 'is_weekend', 'is_night', 'is_business_hours',
            'location_entropy', 'session_duration_mean', 'session_duration_std',
            'data_transferred_mean', 'data_transferred_std', 'location_nunique'
        ]

        df_features = df[feature_cols]
        df_scaled = pd.DataFrame(self.scaler.fit_transform(df_features), columns=feature_cols)

        return df_scaled, df['is_anomaly']

    def train_models(self, df):
        """Train Isolation Forest and Random Forest models"""
        X, y = self.engineer_features(df)

        # Fit Isolation Forest for unsupervised anomaly detection
        self.isolation_forest.fit(X)

        # Fit Random Forest for supervised learning
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.rf_classifier.fit(X_train, y_train)

        y_pred = self.rf_classifier.predict(X_test)
        print("Random Forest Classification Report:\n", classification_report(y_test, y_pred))
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    def save_models(self, path='models/'):
        """Save models to disk"""
        joblib.dump(self.isolation_forest, path + 'isolation_forest.pkl')
        joblib.dump(self.rf_classifier, path + 'rf_classifier.pkl')
        joblib.dump(self.scaler, path + 'scaler.pkl')
        joblib.dump(self.label_encoders, path + 'label_encoders.pkl')
        joblib.dump(self.user_profiles, path + 'user_profiles.pkl')

    def load_models(self, path='models/'):
        """Load models from disk"""
        self.isolation_forest = joblib.load(path + 'isolation_forest.pkl')
        self.rf_classifier = joblib.load(path + 'rf_classifier.pkl')
        self.scaler = joblib.load(path + 'scaler.pkl')
        self.label_encoders = joblib.load(path + 'label_encoders.pkl')
        self.user_profiles = joblib.load(path + 'user_profiles.pkl')

    def predict(self, new_data_df):
        """Predict anomalies on new login data"""
        X_new, _ = self.engineer_features(new_data_df)
        pred_rf = self.rf_classifier.predict(X_new)
        pred_iso = self.isolation_forest.predict(X_new)  # -1 for anomaly, 1 for normal

        # Combine predictions
        final_result = []
        for i in range(len(pred_rf)):
            if pred_rf[i] == 1 or pred_iso[i] == -1:
                final_result.append(1)  # Anomaly
            else:
                final_result.append(0)  # Normal

        return final_result
