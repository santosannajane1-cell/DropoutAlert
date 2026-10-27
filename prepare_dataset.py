
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/student_dropout.csv", sep=";")

# Separate the student information from the target
X = df.drop("Target", axis=1)
y = df["Target"]

# Display the features
print("FEATURES USED FOR PREDICTION")
print(X.columns.tolist())

# Display the target labels
print("\nTARGET LABELS")
print(y.unique())

# Display the number of features
print("\nNUMBER OF FEATURES")
print(X.shape[1])

# Display the number of target labels
print("\nNUMBER OF TARGET LABELS")
print(y.nunique())

# Display the target distribution
print("\nTARGET DISTRIBUTION")
print(y.value_counts())
