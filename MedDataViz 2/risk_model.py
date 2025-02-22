import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Simple risk model using logistic regression
def predict_heart_disease_risk(data):
    # Extract features
    features = np.array([
        float(data.get('blood_pressure', '120/80').split('/')[0]),  # Systolic BP
        float(data.get('blood_pressure', '120/80').split('/')[1]),  # Diastolic BP
        float(data.get('heart_rate', 70)),
        float(data.get('weight', 70))
    ]).reshape(1, -1)
    
    # Normalize features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features)
    
    # Simple logistic regression model
    model = LogisticRegression()
    
    # Dummy training data (in production, this would be properly trained)
    X_train = np.random.rand(100, 4)
    y_train = np.random.randint(0, 2, 100)
    
    model.fit(X_train, y_train)
    
    # Get probability of high risk
    risk_score = model.predict_proba(features_scaled)[0][1]
    
    return float(risk_score)
