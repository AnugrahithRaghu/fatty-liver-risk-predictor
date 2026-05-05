import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# -------- LOAD DATA --------
df = pd.read_csv("data/fatty_liver_dataset.csv")

# -------- ENCODING --------
df["alcohol"] = df["alcohol"].map({"None": 0, "Moderate": 1, "High": 2})
df["activity"] = df["activity"].map({"Low": 0, "Medium": 1, "High": 2})
df["diet"] = df["diet"].map({"Healthy": 0, "Mixed": 1, "Junk": 2})
df["family_history"] = df["family_history"].map({"No": 0, "Yes": 1})
df["risk"] = df["risk"].map({"Low": 0, "Moderate": 1, "High": 2})

# Remove any missing values
df = df.dropna()

# -------- FEATURES --------
X = df.drop("risk", axis=1)
y = df["risk"]

# -------- SPLIT --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------- MODELS --------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier()
}

best_model = None
best_accuracy = 0

# -------- TRAIN --------
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)

    print(f"{name} Accuracy:", acc)

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model

# -------- SAVE MODEL --------
joblib.dump(best_model, "models/fatty_liver_model.pkl")

print("\n✅ Best model saved!")