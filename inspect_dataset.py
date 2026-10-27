
import pandas as pd

# Load the student dataset
df = pd.read_csv("dataset/student_dropout.csv", sep=";")

# Display the dataset size
print("DATASET SIZE")
print(df.shape)

# Display the column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# Display the first 5 student records
print("\nFIRST 5 STUDENT RECORDS")
print(df.head())

# Display student outcomes
print("\nSTUDENT OUTCOMES")
print(df["Target"].value_counts())

# Check for missing values
print("\nMISSING VALUES")
print(df.isnull().sum().sum())
