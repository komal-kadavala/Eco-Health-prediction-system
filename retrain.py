import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import joblib

print("Loading data...")
h = pd.read_csv("cleaned_health_data_final.csv")
x = h.drop(["Diabetes_Risk","Heart_Disease_Risk","Obesity_Risk","HealthRisk","Height_cm","Weight_kg","BMI","Blood_Sugar_mg_dL","Systolic_BP","Diastolic_BP"], axis=1)
y = h["Heart_Disease_Risk"]

print("Fitting scaler...")
scaler = StandardScaler()
scaler.fit(x)

print("Training Heart Disease model...")
model = DecisionTreeClassifier(random_state=42)
model.fit(x, y)

print("Saving Heart Disease model and scaler...")
joblib.dump(model, "Heart_Disease_Risk.pkl")
joblib.dump(scaler, "Heart_Disease_scaler.pkl")
print("Done.")
