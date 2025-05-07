import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("traffic.sqlite3")

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database file not found at: {DB_PATH.resolve()}")

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

print("📋 Tables found in the database:")
for table in tables:
    print(f"  - {table[0]}")


# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("📋 Tables found:")
for table in tables:
    print(f"  - {table[0]}")

# Example: Read first 5 rows from each table
for (table_name,) in tables:
    print(f"\n🔍 Reading rows from: {table_name}")
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


cursor.execute("PRAGMA table_info(traffic_data);")
schema = cursor.fetchall()

for column in schema:
    print(column)

# Close the connection
conn.close()