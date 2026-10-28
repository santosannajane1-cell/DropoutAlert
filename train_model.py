
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

# =====================================
# 1. LOAD ORIGINAL DATASET
# =====================================

df = pd.read_csv("dataset/student_dropout.csv", sep=";")

print("Original dataset loaded successfully!")
print("Dataset shape:", df.shape)


# =====================================
# 2. CONVERT GRADES TO 0-100 SCALE
# =====================================

# Admission Grade: 0-200 becomes 0-100
df["Admission grade"] = df["Admission grade"] / 2

# First Semester Grade: 0-20 becomes 0-100
df["Curricular units 1st sem (grade)"] = (
    df["Curricular units 1st sem (grade)"] * 5
)

# Save converted dataset without changing the original
df.to_csv(
    "dataset/student_dropout_100.csv",
    sep=";",
    index=False
)

print("\nGrades converted to 0-100 scale.")
print("Converted dataset saved to:")
print("dataset/student_dropout_100.csv")


# =====================================
# 3. SELECT FEATURES
# =====================================

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
# Graduate or Enrolled = 0 (Not At Risk)
y = (df["Target"] == "Dropout").astype(int)


# =====================================
# 4. SPLIT DATASET
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nDataset split completed.")
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# =====================================
# 5. TRAIN RANDOM FOREST MODEL
# =====================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nModel training completed!")


# =====================================
# 6. MODEL EVALUATION
# =====================================

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_prob)

report = classification_report(
    y_test,
    y_pred,
    target_names=["Not At Risk", "At Risk"]
)

matrix = confusion_matrix(y_test, y_pred)

print("\nMODEL EVALUATION")
print("----------------------")
print(f"Accuracy: {accuracy:.4f}")
print(f"Recall:   {recall:.4f}")
print(f"ROC-AUC: {roc_auc:.4f}")

print("\nCLASSIFICATION REPORT")
print(report)

print("\nCONFUSION MATRIX")
print(matrix)


# =====================================
# 7. SAVE MODEL AND FEATURES
# =====================================

os.makedirs("model", exist_ok=True)
os.makedirs("evaluation", exist_ok=True)

with open("model/dropout_model.pkl", "wb") as file:
    pickle.dump(model, file)

with open("model/features.pkl", "wb") as file:
    pickle.dump(features, file)

print("\nModel saved successfully!")
print("Location: model/dropout_model.pkl")


# =====================================
# 8. SAVE EVALUATION RESULTS
# =====================================

evaluation_results = {
    "accuracy": float(accuracy),
    "recall": float(recall),
    "roc_auc": float(roc_auc),
    "classification_report": report,
    "confusion_matrix": matrix.tolist(),
    "features": features,
    "hyperparameters": {
        "model": "RandomForestClassifier",
        "n_estimators": 100,
        "random_state": 42,
        "class_weight": "balanced"
    }
}

with open(
    "evaluation/evaluation_results.json",
    "w"
) as file:
    json.dump(evaluation_results, file, indent=4)

with open(
    "evaluation/evaluation_report.txt",
    "w"
) as file:
    file.write("MODEL EVALUATION\n")
    file.write("----------------------\n")
    file.write(f"Accuracy: {accuracy:.4f}\n")
    file.write(f"Recall:   {recall:.4f}\n")
    file.write(f"ROC-AUC: {roc_auc:.4f}\n\n")
    file.write("CLASSIFICATION REPORT\n")
    file.write(report)
    file.write("\nCONFUSION MATRIX\n")
    file.write(str(matrix))

print("\nEvaluation results saved!")


# =====================================
# 9. SHOW TEST EXAMPLES
# =====================================

print("\nSAMPLE TEST PREDICTIONS")
print("----------------------")

test_samples = X_test.head(5)

sample_predictions = model.predict(test_samples)
sample_probabilities = model.predict_proba(test_samples)[:, 1]

for i in range(len(test_samples)):
    prediction = (
        "At Risk"
        if sample_predictions[i] == 1
        else "Not At Risk"
    )

    risk_percentage = sample_probabilities[i] * 100

    print(f"\nStudent {i + 1}")
    print("Prediction:", prediction)
    print(f"Risk Percentage: {risk_percentage:.2f}%")


# =====================================
# 10. DATASET CHECKS
# =====================================

print("\nDATASET CHECKS")
print("----------------------")

print("Duplicate records:", df.duplicated().sum())

print(
    "Target included in features:",
    "Target" in features
)

print(
    "Matching feature rows between train and test:",
    X_train.index.isin(X_test.index).sum()
)

print(
    "Matching full records between train and test:",
    df.loc[X_train.index].isin(
        df.loc[X_test.index]
    ).all(axis=1).sum()
)

print("\nALL DONE! MODEL TRAINING COMPLETED!")
