import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import glob

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

# Function to create a new sheet or update an existing one with data from the file
def update_sheet(file_path, spreadsheet):
    print(f"Processing file: {file_path}")  # Debugging

    # Read the file based on its extension
    try:
        if file_path.endswith('.xlsx'):
            data = pd.read_excel(file_path, engine='openpyxl')
        elif file_path.endswith('.csv'):
            data = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    # Convert all data to string to avoid JSON serialization issues
    data = data.astype(str)

    # Create a new sheet or update an existing one for this file
    sheet_title = os.path.basename(file_path).split('.')[0]  # Use file name as sheet title
    try:
        if sheet_title in [sheet.title for sheet in spreadsheet.worksheets()]:
            print(f"Sheet '{sheet_title}' already exists. Updating the existing sheet.")
            sheet = spreadsheet.worksheet(sheet_title)
        else:
            sheet = spreadsheet.add_worksheet(title=sheet_title, rows="100", cols="20")
            print(f"Created new sheet: {sheet_title}")
    except Exception as e:
        print(f"Error processing sheet: {e}")
        return

    # Convert DataFrame to list of lists, for uploading to Sheets
    # Include headers in the upload
    data_to_upload = [data.columns.tolist()] + data.values.tolist()

    # Update the sheet with the data
    try:
        response = sheet.update('A1', data_to_upload, value_input_option='USER_ENTERED')
        print(f"Updated sheet '{sheet_title}' with data. Response: {response}")
    except Exception as e:
        print(f"Error updating sheet '{sheet_title}': {e}")

# Directory containing your .csv and .xlsx files
file_directory = '[path_to_your_directory]'

# List of all .csv and .xlsx files
file_paths = glob.glob(file_directory + "/*.csv") + glob.glob(file_directory + "/*.xlsx")

# Update the sheet with each file
for file_path in file_paths:
    update_sheet(file_path, spreadsheet)
