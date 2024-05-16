import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuration
SERVICE_ACCOUNT_FILE = '/Users/tis/foam/cdp/code/cfg/Seotieto.json'
SHEET_ID = 'SHEET_ID'
SHEET_NAME = '1'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Use creds to create a client to interact with the Google Drive API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Spreadsheet
spreadsheet = client.open_by_key(SHEET_ID)

# Get the worksheet
worksheet = spreadsheet.worksheet(SHEET_NAME)

# Get all values from the worksheet and convert to a DataFrame
data = worksheet.get_all_values()
df = pd.DataFrame(data[1:], columns=data[0])

# Check for duplicates in the 'full_name' and 'company_name' columns and keep only 'full_name', 'company_name' and 'key' columns
duplicates = df[df.duplicated(['full_name', 'company_name'])][['full_name', 'company_name', 'key']]

# Print the duplicates
print(duplicates)
