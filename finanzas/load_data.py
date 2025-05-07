import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def load_env(filepath="../.env"):

    with open(filepath) as f:

        for line in f:

            if line.strip() and not line.startswith("#"):

                key, _, value = line.strip().partition("=")
                os.environ[key] = value

# Load the .env file manually
load_env()

# get environment variables
KEY_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")
SHEET_ID = os.getenv('FINANZAS_SHEET_ID')

# Set up scopes and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)

# Authorize client
client = gspread.authorize(creds)

def get_sheet_by_gid(gid):
    spreadsheet = client.open_by_key(SHEET_ID)
    return spreadsheet.get_worksheet_by_id(gid)


