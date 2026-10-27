
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/student_dropout.csv", sep=";")

# Display all available columns
print("AVAILABLE FEATURES")
for column in df.columns:
    print(column)

# Display the target
print("\nTARGET COLUMN")
print(df["Target"].value_counts())
