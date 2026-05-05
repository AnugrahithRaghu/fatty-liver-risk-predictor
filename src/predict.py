import joblib
import numpy as np

# Load model
model = joblib.load("models/fatty_liver_model.pkl")

# Example input
# age, height, weight, bmi, waist,
# alcohol, activity, diet, family_history,
# alt, ast, cholesterol, triglycerides, sugar

input_data = np.array([[ 
    45, 170, 85, 29.4, 102,
    2, 0, 2, 1,
    60, 55, 250, 300, 140
]])

prediction = model.predict(input_data)[0]

risk_map = {0: "Low", 1: "Moderate", 2: "High"}

print("Predicted Risk:", risk_map[prediction])