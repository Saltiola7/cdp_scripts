import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv('/Users/tis/foam/cdp/function/util/Sheets/.env')

# Retrieve environment variables
SERVICE_ACCOUNT_KEY_PATH = os.getenv("SERVICE_ACCOUNT_KEY_PATH")
SPREADSHEET_URL = os.getenv("SPREADSHEET_URL")

# Use credentials to create a client to interact with the Google Drive API
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_KEY_PATH, scope)
client = gspread.authorize(creds)

# Open the spreadsheet
spreadsheet = client.open_by_url(SPREADSHEET_URL)

# Iterate through each sheet in the spreadsheet and freeze the first row
for sheet in spreadsheet.worksheets():
    sheet.freeze(rows=1)
    print(f"Froze the first row in '{sheet.title}'")

print("All sheets processed.")
