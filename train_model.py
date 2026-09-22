import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# --------------------------------
# 1. Load Dataset
# --------------------------------

data = pd.read_csv("data/symptoms.csv")

print("Dataset loaded successfully.")
print("Dataset shape:", data.shape)


# --------------------------------
# 2. Separate Features and Target
# --------------------------------

X = data.drop("possible_category", axis=1)

y = data["possible_category"]


# --------------------------------
# 3. Train/Test Split
# --------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)


# --------------------------------
# 4. Create Model
# --------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# --------------------------------
# 5. Train Model
# --------------------------------

model.fit(X_train, y_train)

print("Model training completed.")


# --------------------------------
# 6. Make Predictions
# --------------------------------

y_pred = model.predict(X_test)


# --------------------------------
# 7. Evaluate Model
# --------------------------------

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(accuracy)


print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))


print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# --------------------------------
# 8. Save Model
# --------------------------------

joblib.dump(
    model,
    "models/symptom_model.pkl"
)

print("\nModel saved successfully!")
print("Location: models/symptom_model.pkl")