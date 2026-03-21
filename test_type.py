import joblib

base_dir = r"C:\Desktop\K Project main\K Project 01\K Project 02"

try:
    heart_m = joblib.load(f"{base_dir}\\Heart_Disease_Risk.pkl")
    heart_s = joblib.load(f"{base_dir}\\Heart_Disease_scaler.pkl")
    print(f"Heart_Disease_Risk.pkl type: {type(heart_m)}")
    print(f"Heart_Disease_scaler.pkl type: {type(heart_s)}")
    
    obesity_m = joblib.load(f"{base_dir}\\Obesity_model.pkl")
    obesity_s = joblib.load(f"{base_dir}\\Obesity_scaler.pkl")
    print(f"Obesity_model.pkl type: {type(obesity_m)}")
    print(f"Obesity_scaler.pkl type: {type(obesity_s)}")
except Exception as e:
    print(e)
