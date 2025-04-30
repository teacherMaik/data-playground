import requests
import csv
import io
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def load_env(filepath="../.env"):
    import os
    with open(filepath) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, _, value = line.strip().partition("=")
                os.environ[key] = value

# Load the .env file manually
load_env()

# Now this will work
KEY_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")
print("Path to key:", KEY_PATH)

SHEET_ID = os.getenv('FINANZAS_SHEET_ID')
print(id)

GID = 191174433
# Set up scopes and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)

# Authorize client
client = gspread.authorize(creds)

# Open sheet by ID and get specific worksheet by gid
spreadsheet = client.open_by_key(SHEET_ID)

# Find the worksheet with gid
for worksheet in spreadsheet.worksheets():
    print(worksheet.id)
    if worksheet.id == GID:
        data = worksheet.get_all_values()
        break
else:
    raise ValueError(f"Worksheet with gid {GID} not found")

# Print retrieved data
for row in data:
    print(row)

# print(get_sheet_id('FINANZAS_SHEET_ID'))

# SHEET_ID = get_sheet_id('FINANZAS_SHEET_ID')
# 
# URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

# response = requests.get(URL)

# if response.status_code == 200:
#     data = response.content.decode('utf-8')
#     reader = csv.reader(io.StringIO(data))
#     rows = list(reader)
#     for row in rows:
#         print(row)
# else:
#     print(f"Failed to fetch data: {response.status_code}")
