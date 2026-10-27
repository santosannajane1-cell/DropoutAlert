
import pandas as pd
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    recall_score,
    roc_auc_score
)

# Load the dataset
df = pd.read_csv("dataset/student_dropout.csv", sep=";")

# Select early-warning features
features = [
    "Admission grade",
    "Age at enrollment",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (evaluations)"
]

# Prepare the input data
X = df[features]

# Convert the target into binary labels
# Dropout = 1 (At Risk)
# Graduate or Enrolled = 0 (Not At Risk)
y = (df["Target"] == "Dropout").astype(int)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

# Train the model
model.fit(X_train, y_train)

# Predict using unseen test data
y_pred = model.predict(X_test)

# Get probability of being at risk
y_prob = model.predict_proba(X_test)[:, 1]

# Evaluate the model
print("\nMODEL EVALUATION")
print("----------------------")

print("Recall:", recall_score(y_test, y_pred))

print("ROC-AUC:", roc_auc_score(y_test, y_prob))

print("\nCLASSIFICATION REPORT")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Not At Risk", "At Risk"]
))

print("\nCONFUSION MATRIX")
print(confusion_matrix(y_test, y_pred))

# Save the trained model
os.makedirs("model", exist_ok=True)

with open("model/dropout_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save the feature names
with open("model/features.pkl", "wb") as file:
    pickle.dump(features, file)

print("\nModel saved successfully!")
