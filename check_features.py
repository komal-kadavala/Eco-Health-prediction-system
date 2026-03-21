import joblib
import pandas as pd

base_dir = r"C:\Desktop\K Project main\K Project 01\K Project 02"
models = ['Diabetes_Risk.pkl', 'Heart_Disease_Risk.pkl', 'Obesity_model.pkl']

for m in models:
    try:
        model = joblib.load(f"{base_dir}\\{m}")
        if hasattr(model, 'feature_names_in_'):
            print(f"{m} features: {model.feature_names_in_}")
        else:
            print(f"{m} - No feature_names_in_ attribute.")
    except Exception as e:
        print(f"Error loading {m}: {e}")
