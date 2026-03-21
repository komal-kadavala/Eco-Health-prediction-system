import joblib
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

base_dir = r"C:\Desktop\K Project main\K Project 01\K Project 02"

try:
    diabetes_model = joblib.load(f"{base_dir}\\Diabetes_Risk.pkl")
    diabetes_scaler = joblib.load(f"{base_dir}\\Diabetes_scaler.pkl")
    
    diab_features = pd.DataFrame([[30, 1, 170.0, 70.0, 24.2, 100.0, 120, 80, 180.0, 0, 2.0, 0, 8.0, 5.0]], 
                                columns=['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI', 'Blood_Sugar_mg_dL', 'Systolic_BP', 'Diastolic_BP', 'Cholesterol_mg_dL', 'Smoking', 'Exercise_Hours_per_Week', 'Family_History', 'Sleep_Hours', 'Stress_Level_1_to_10'])
    diab_scaled = diabetes_scaler.transform(diab_features)
    diabetes_prob = float(diabetes_model.predict_proba(diab_scaled)[0][1] * 100)
    print(f"Diabetes Prob: {diabetes_prob}")

    heart_model = joblib.load(f"{base_dir}\\Heart_Disease_Risk.pkl")
    heart_scaler = joblib.load(f"{base_dir}\\Heart_Disease_scaler.pkl")
    heart_features = pd.DataFrame([[30, 1, 180.0, 0, 2.0, 0, 8.0, 5.0]], 
                                columns=['Age', 'Gender', 'Cholesterol_mg_dL', 'Smoking', 'Exercise_Hours_per_Week', 'Family_History', 'Sleep_Hours', 'Stress_Level_1_to_10'])
    heart_scaled = heart_scaler.transform(heart_features)
    heart_prob = float(heart_model.predict_proba(heart_scaled)[0][1] * 100)
    print(f"Heart Prob: {heart_prob}")

    obesity_model = joblib.load(f"{base_dir}\\Obesity_model.pkl")
    obesity_scaler = joblib.load(f"{base_dir}\\Obesity_scaler.pkl")
    obesity_features = pd.DataFrame([[30, 1, 170.0, 70.0, 24.2, 100.0, 120, 80, 180.0, 0, 2.0, 0, 8.0, 5.0]], 
                                columns=['Age', 'Gender', 'Height_cm', 'Weight_kg', 'BMI', 'Blood_Sugar_mg_dL', 'Systolic_BP', 'Diastolic_BP', 'Cholesterol_mg_dL', 'Smoking', 'Exercise_Hours_per_Week', 'Family_History', 'Sleep_Hours', 'Stress_Level_1_to_10'])
    obesity_scaled = obesity_scaler.transform(obesity_features)
    obesity_prob = float(obesity_model.predict_proba(obesity_scaled)[0][1] * 100)
    print(f"Obesity Prob: {obesity_prob}")
except Exception as e:
    print(f"Error: {e}")
