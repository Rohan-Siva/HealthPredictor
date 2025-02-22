import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Load and prepare the diabetes prediction model
diabetes_data = pd.read_csv('diabetes_prediction_dataset.csv')
X = diabetes_data[['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease', 'smoking_history']]

# Convert smoking_history to numeric using one-hot encoding
X = pd.get_dummies(X, columns=['smoking_history'], prefix='smoking')

y = diabetes_data['diabetes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
diabetes_scaler = StandardScaler()
X_train_scaled = diabetes_scaler.fit_transform(X_train)
X_test_scaled = diabetes_scaler.transform(X_test)

diabetes_model = RandomForestClassifier(random_state=42)
diabetes_model.fit(X_train_scaled, y_train)

# Get the smoking history categories from the training data
smoking_categories = [col.replace('smoking_', '') for col in X.columns if col.startswith('smoking_')]

def predict_diabetes_risk(data):
    """
    Predict diabetes risk based on input features

    Args:
        data (dict): Dictionary containing patient health data including:
            - age
            - bmi
            - hba1c_level
            - blood_glucose_level
            - hypertension (0 or 1)
            - heart_disease (0 or 1)
            - smoking_history (string)

    Returns:
        float: Probability of diabetes (risk score between 0 and 1)
    """
    try:
        # Create feature array with zeros for smoking categories
        feature_dict = {
            'age': float(data['age']),
            'bmi': float(data['bmi']),
            'HbA1c_level': float(data['hba1c_level']),
            'blood_glucose_level': float(data['blood_glucose_level']),
            'hypertension': int(data['hypertension']),
            'heart_disease': int(data['heart_disease'])
        }

        # Add smoking history one-hot encoded columns
        smoking_status = data['smoking_history']
        for category in smoking_categories:
            feature_dict[f'smoking_{category}'] = 1 if smoking_status == category else 0

        # Convert to DataFrame to ensure correct feature order
        features_df = pd.DataFrame([feature_dict])
        features_df = features_df.reindex(columns=X.columns, fill_value=0)

        # Scale features and predict
        features_scaled = diabetes_scaler.transform(features_df)
        risk_score = diabetes_model.predict_proba(features_scaled)[0][1]

        return float(risk_score)
    except Exception as e:
        raise Exception(f"Error predicting diabetes risk: {str(e)}")