import streamlit as st
import joblib
import numpy as np

# -------- LOAD MODEL --------
model = joblib.load("models/fatty_liver_model.pkl")

st.title("Fatty Liver Risk Predictor (Lab + Lifestyle) 🩺")

st.warning("⚠️ This is not a medical diagnosis. Consult a doctor.")

# -------- BASIC INPUTS --------
st.subheader("Basic Information")

age = st.slider("Age", 18, 70)
height = st.slider("Height (cm)", 140, 200)
weight = st.slider("Weight (kg)", 40, 120)

# BMI
bmi = weight / ((height / 100) ** 2)
st.write("BMI:", round(bmi, 2))

# -------- WAIST (AUTO FROM JEANS) --------
st.subheader("Waist Input 👖")

if "waist" not in st.session_state:
    st.session_state.waist = 70

jeans_size = st.selectbox(
    "Select your jeans size (optional)",
    ["None"] + [str(s) for s in range(26, 54, 2)]
)

if jeans_size != "None":
    st.session_state.waist = round(int(jeans_size) * 2.54)

waist = st.slider("Waist Circumference (cm)", 60, 130, value=st.session_state.waist)

# -------- LIFESTYLE --------
st.subheader("Lifestyle")

alcohol = st.selectbox("Alcohol Consumption", ["None", "Moderate", "High"])
activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"])
diet = st.selectbox("Diet Type", ["Healthy", "Mixed", "Junk"])
family_history = st.selectbox("Family History", ["No", "Yes"])

# -------- LAB VALUES --------
st.subheader("Lab Report Values 🧪")

alt = st.slider("ALT (SGPT)", 10, 150)
ast = st.slider("AST (SGOT)", 10, 150)
cholesterol = st.slider("Cholesterol", 100, 350)
triglycerides = st.slider("Triglycerides", 50, 400)
sugar = st.slider("Fasting Blood Sugar", 70, 200)

# -------- ENCODING --------
alcohol_map = {"None": 0, "Moderate": 1, "High": 2}
activity_map = {"Low": 0, "Medium": 1, "High": 2}
diet_map = {"Healthy": 0, "Mixed": 1, "Junk": 2}
family_map = {"No": 0, "Yes": 1}

# -------- PREDICTION --------
if st.button("Predict"):
    input_data = np.array([[
        age, height, weight, bmi, waist,
        alcohol_map[alcohol],
        activity_map[activity],
        diet_map[diet],
        family_map[family_history],
        alt, ast, cholesterol, triglycerides, sugar
    ]])

    prediction = model.predict(input_data)[0]

    risk_map = {0: "Low", 1: "Moderate", 2: "High"}
    result = risk_map[prediction]

    st.subheader(f"Risk Level: {result}")

    # -------- EXPLANATION --------
    reasons = []

    if bmi > 30:
        reasons.append("High BMI (Obesity)")
    elif bmi > 25:
        reasons.append("Overweight")

    if waist > 100:
        reasons.append("High Waist Circumference")

    if alcohol == "High":
        reasons.append("High Alcohol Consumption")

    if activity == "Low":
        reasons.append("Low Physical Activity")

    if diet == "Junk":
        reasons.append("Unhealthy Diet")

    if family_history == "Yes":
        reasons.append("Family History")

    if alt > 40:
        reasons.append("High ALT (Liver Enzyme)")

    if ast > 40:
        reasons.append("High AST")

    if triglycerides > 200:
        reasons.append("High Triglycerides")

    if cholesterol > 240:
        reasons.append("High Cholesterol")

    if sugar > 126:
        reasons.append("High Blood Sugar")

    # -------- SHOW RESULT --------
    if result == "High":
        st.error("⚠️ High Risk")
    elif result == "Moderate":
        st.warning("⚠️ Moderate Risk")
    else:
        st.success("✅ Low Risk")

    # -------- SHOW REASONS --------
    if reasons:
        st.markdown("### 🔍 Why this result?")
        for r in reasons:
            st.write("•", r)

    # -------- RECOMMENDATIONS --------
    st.markdown("### 💡 Recommendations")

    if result == "High":
        st.write("• Reduce alcohol")
        st.write("• Improve diet")
        st.write("• Exercise regularly")
        st.write("• Consult a doctor")

    elif result == "Moderate":
        st.write("• Maintain healthy diet")
        st.write("• Stay active")
        st.write("• Monitor health")

    else:
        st.write("• Keep your lifestyle 👍")