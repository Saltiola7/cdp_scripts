import pandas as pd
import gspread
import numpy as np
from google.oauth2.service_account import Credentials

# Configuration
SERVICE_ACCOUNT_FILE = '/Users/tis/foam/cdp/code/cfg/Seotieto.json'
SHEET_ID = 'SHEET_ID'
SOURCE_SHEET_NAME = 'source_sheet_name'
DESTINATION_SHEET_NAME = '1'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Use creds to create a client to interact with the Google Drive API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Spreadsheet
spreadsheet = client.open_by_key(SHEET_ID)

# Get the source and destination worksheets
source_worksheet = spreadsheet.worksheet(SOURCE_SHEET_NAME)
destination_worksheet = spreadsheet.worksheet(DESTINATION_SHEET_NAME)

# Get all values from the source worksheet and convert to a DataFrame
source_data = source_worksheet.get_all_values()
source_df = pd.DataFrame(source_data[1:], columns=source_data[0])

# Get all values from the destination worksheet and convert to a DataFrame
destination_data = destination_worksheet.get_all_values()
destination_df = pd.DataFrame(destination_data[1:], columns=destination_data[0])

# Check if each column in the destination DataFrame exists in the source DataFrame
common_columns = [col for col in destination_df.columns if col in source_df.columns]

# Reorder the columns of the source DataFrame to match the common columns in the destination DataFrame
source_df = source_df[common_columns]

# Append the source DataFrame to the destination DataFrame
combined_df = pd.concat([destination_df, source_df])

# Replace infinite values with None
combined_df = combined_df.replace([np.inf, -np.inf], None)

# Replace NaN values with None
combined_df = combined_df.where(pd.notnull(combined_df), None)

# Append the new data to the destination worksheet
destination_worksheet.append_rows(combined_df[destination_df.shape[0]:].values.tolist())
