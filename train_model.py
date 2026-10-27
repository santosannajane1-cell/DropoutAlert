
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

print("\nCLASS DISTRIBUTION AND SPLIT")
print("Total records:", len(y))
print("Training records:", len(y_train))
print("Testing records:", len(y_test))

print("\nFull dataset:")
print(y.value_counts().sort_index())

print("\nTraining:")
print(y_train.value_counts().sort_index())

print("\nTesting:")
print(y_test.value_counts().sort_index())

# 5. Evaluate on unseen test data
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# DISPLAY 4 ACTUAL TESTING SAMPLES
print("\nTESTING SAMPLES")
print("=" * 50, flush=True)

samples = X_test.head(4).copy()
actual = y_test.loc[samples.index]
predicted = model.predict(samples)

for i in range(len(samples)):
    print(f"\nSample {i + 1}", flush=True)
    print(samples.iloc[i].to_string(), flush=True)

    expected = "At Risk" if actual.iloc[i] == 1 else "Not At Risk"
    prediction = "At Risk" if predicted[i] == 1 else "Not At Risk"
    correct = "Yes" if actual.iloc[i] == predicted[i] else "No"

    print(f"Expected: {expected}", flush=True)
    print(f"Predicted: {prediction}", flush=True)
    print(f"Correct: {correct}", flush=True)

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

# DUPLICATE AND LEAKAGE CHECK

print("\nDUPLICATE AND LEAKAGE CHECK")
print("---------------------------")

# 1. Check duplicate records in the full dataset
duplicates = df.duplicated().sum()
print("Duplicate records:", duplicates)

# 2. Check whether the target column is used as an input feature
print("Target included in features:", "Target" in features)

# 3. Check for identical feature rows across training and testing
overlap = X_train.merge(X_test, how="inner").shape[0]
print("Matching feature rows across train/test:", overlap)

# Check exact full-record overlap between train and test
train_rows = df.loc[X_train.index]
test_rows = df.loc[X_test.index]

full_record_overlap = train_rows.merge(
    test_rows,
    how="inner"
).shape[0]

print("Matching full records across train/test:", full_record_overlap)