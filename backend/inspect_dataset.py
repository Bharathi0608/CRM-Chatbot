import pandas as pd

file_path = "../data/accounts.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET INFO ==========\n")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n========== COLUMNS ==========\n")

for column in df.columns:
    print(column)

print("\n========== FIRST 5 ROWS ==========\n")

print(df.head())

print("\n========== DATA TYPES ==========\n")

print(df.dtypes)

print("\n========== MISSING VALUES ==========\n")

print(df.isnull().sum())