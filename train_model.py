
import pandas as pd
import pickle
import os
import json

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    recall_score,
    roc_auc_score,
    accuracy_score
)

# 1. Load dataset
df = pd.read_csv("dataset/student_dropout.csv", sep=";")

# 2. Select early-warning features
features = [
    "Admission grade",
    "Age at enrollment",
    "Curricular units 1st sem (enrolled)",
    "Curricular units 1st sem (approved)",
    "Curricular units 1st sem (grade)",
    "Curricular units 1st sem (evaluations)"
]

X = df[features]

# Dropout = 1 (At Risk)
# Graduate and Enrolled = 0 (Not At Risk)
y = (df["Target"] == "Dropout").astype(int)

# 3. Split dataset: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 4. Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# 5. Evaluate on unseen test data
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

report = classification_report(
    y_test,
    y_pred,
    target_names=["Not At Risk", "At Risk"],
    output_dict=True,
    zero_division=0
)

matrix = confusion_matrix(y_test, y_pred)

# 6. Display evaluation results
print("\nMODEL EVALUATION")
print("----------------------")
print(f"Accuracy: {accuracy:.4f}")
print(f"Recall:   {recall:.4f}")
print(f"ROC-AUC:  {roc_auc:.4f}")

print("\nCLASSIFICATION REPORT")
print(classification_report(
    y_test,
    y_pred,
    target_names=["Not At Risk", "At Risk"],
    zero_division=0
))

print("\nCONFUSION MATRIX")
print(matrix)

# 7. Save model, features, and evaluation results
os.makedirs("model", exist_ok=True)
os.makedirs("evaluation", exist_ok=True)

with open("model/dropout_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("model/features.pkl", "wb") as file:
    pickle.dump(features, file)

results = {
    "dataset_rows": int(len(df)),
    "training_rows": int(len(X_train)),
    "testing_rows": int(len(X_test)),
    "accuracy": float(accuracy),
    "recall": float(recall),
    "roc_auc": float(roc_auc),
    "classification_report": report,
    "confusion_matrix": matrix.tolist(),
    "features": features,
    "target_definition": {
        "1": "At Risk (Dropout)",
        "0": "Not At Risk (Graduate or Enrolled)"
    }
}

with open("evaluation/evaluation_results.json", "w") as file:
    json.dump(results, file, indent=4)

with open("evaluation/evaluation_report.txt", "w") as file:
    file.write("DROPOUTALERT MODEL EVALUATION\n")
    file.write("============================\n\n")
    file.write(f"Dataset records: {len(df)}\n")
    file.write(f"Training records: {len(X_train)}\n")
    file.write(f"Testing records: {len(X_test)}\n\n")
    file.write(f"Accuracy: {accuracy:.4f}\n")
    file.write(f"Recall: {recall:.4f}\n")
    file.write(f"ROC-AUC: {roc_auc:.4f}\n\n")
    file.write("CLASSIFICATION REPORT\n")
    file.write(classification_report(
        y_test,
        y_pred,
        target_names=["Not At Risk", "At Risk"],
        zero_division=0
    ))
    file.write("\nCONFUSION MATRIX\n")
    file.write(str(matrix))
    file.write("\n")

print("\nModel saved successfully!")
print("Evaluation results saved in the evaluation folder.")
