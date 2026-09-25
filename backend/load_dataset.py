import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

CSV_FILE = "../data/accounts.csv"

print("Loading CRM dataset...")

df = pd.read_csv(CSV_FILE)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nColumns:")
for column in df.columns:
    print(f"- {column}")

print("\nConnecting to PostgreSQL...")

engine = create_engine(DATABASE_URL)

print("Uploading dataset...")

df.to_sql(
    "accounts",
    engine,
    if_exists="replace",
    index=False
)

print("\n===================================")
print("CRM DATASET IMPORTED SUCCESSFULLY")
print("===================================")

print("Table: accounts")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")