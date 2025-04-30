import requests
import csv
import io
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

KEY_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_KEY_PATH")
SHEET_ID = os.getenv('FINANZAS_SHEET_ID')

INGRESOS_GASTOS_GID = 191174433
ACCIONES_GID = 350985506

# Set up scopes and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_PATH, scope)

# Authorize client
client = gspread.authorize(creds)

# Open sheet by ID and get specific worksheet by gid
spreadsheet = client.open_by_key(SHEET_ID)

ingresos_gastos_spreadsheet = spreadsheet.get_worksheet_by_id(INGRESOS_GASTOS_GID)
acciones_spreadsheet = spreadsheet.get_worksheet_by_id(ACCIONES_GID)

ingresos_gastos_data = ingresos_gastos_spreadsheet.get_all_values()
acciones_data = acciones_spreadsheet.get_all_values()

