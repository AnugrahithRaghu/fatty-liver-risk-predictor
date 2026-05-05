import random
import pandas as pd

def calculate_bmi(weight, height):
    return weight / ((height / 100) ** 2)

def generate_data(n=1000):
    data = []

    for _ in range(n):
        # -------- BASIC --------
        age = random.randint(18, 70)
        height = random.randint(150, 190)
        weight = random.randint(45, 110)

        bmi = calculate_bmi(weight, height)
        waist = random.randint(70, 120)

        # -------- LIFESTYLE --------
        alcohol = random.choice(["None", "Moderate", "High"])
        activity = random.choice(["Low", "Medium", "High"])
        diet = random.choice(["Healthy", "Mixed", "Junk"])
        family_history = random.choice(["Yes", "No"])

        # -------- LAB VALUES --------
        alt = random.randint(10, 120)              # Liver enzyme
        ast = random.randint(10, 120)              # Liver enzyme
        cholesterol = random.randint(120, 300)
        triglycerides = random.randint(80, 400)
        sugar = random.randint(70, 180)

        # -------- SCORING SYSTEM --------
        score = 0

        # BMI
        if bmi > 30:
            score += 3
        elif bmi > 25:
            score += 2

        # Waist
        if waist > 100:
            score += 3

        # Alcohol
        if alcohol == "High":
            score += 3
        elif alcohol == "Moderate":
            score += 1

        # Activity
        if activity == "Low":
            score += 2

        # Diet
        if diet == "Junk":
            score += 2

        # Family history
        if family_history == "Yes":
            score += 2

        # Age
        if age > 50:
            score += 2

        # -------- LAB SCORING --------
        if alt > 40:
            score += 3

        if ast > 40:
            score += 2

        if triglycerides > 200:
            score += 3

        if cholesterol > 240:
            score += 2

        if sugar > 126:
            score += 2

        # -------- FINAL RISK --------
        if score <= 5:
            risk = "Low"
        elif score <= 12:
            risk = "Moderate"
        else:
            risk = "High"

        data.append([
            age, height, weight, bmi, waist,
            alcohol, activity, diet, family_history,
            alt, ast, cholesterol, triglycerides, sugar,
            risk
        ])

    columns = [
        "age", "height", "weight", "bmi", "waist",
        "alcohol", "activity", "diet", "family_history",
        "alt", "ast", "cholesterol", "triglycerides", "sugar",
        "risk"
    ]

    return pd.DataFrame(data, columns=columns)


# -------- RUN --------
df = generate_data(1000)

df.to_csv("data/fatty_liver_dataset.csv", index=False)

print("✅ Dataset created successfully!")