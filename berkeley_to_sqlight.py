from berkeleydb import db
import sqlite3
from pathlib import Path

# --- Locate paths ---
# This script runs in /app inside the Docker container (based on Dockerfile WORKDIR)
berkeley_db_path = Path("traffic_berk.db")

# Save SQLite DB two levels below (e.g. ../../converted/traffic.sqlite3)
output_sqlite_path = Path("/app/ludo-web/ludo-web-traffic/traffic.sqlite3")
output_sqlite_path.parent.mkdir(parents=True, exist_ok=True)

# --- Read Berkeley DB ---
bdb = db.DB()
bdb.open(str(berkeley_db_path), None, db.DB_HASH, db.DB_RDONLY)

data = {}
cursor = bdb.cursor()
rec = cursor.first()
while rec:
    key, value = rec
    data[key.decode()] = value.decode()
    rec = cursor.next()
bdb.close()

print(f"Loaded {len(data)} records from Berkeley DB.")

# --- Write to SQLite ---
conn = sqlite3.connect(output_sqlite_path)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS traffic_data (key TEXT PRIMARY KEY, value TEXT)")

for key, value in data.items():
    cur.execute("INSERT OR REPLACE INTO traffic_data (key, value) VALUES (?, ?)", (key, value))

conn.commit()
conn.close()

print(f"Data exported to SQLite at: {output_sqlite_path}")
