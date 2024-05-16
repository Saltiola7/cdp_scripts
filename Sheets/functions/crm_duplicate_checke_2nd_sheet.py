import gspread
from google.oauth2.service_account import Credentials

# Configuration
SERVICE_ACCOUNT_FILE = '/Users/tis/foam/cdp/code/cfg/Seotieto.json'
SHEET_ID = 'SHEET_ID'
SOURCE_SHEET_NAME = 'Instantly'
TARGET_SHEET_NAME = '1'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Use creds to create a client to interact with the Google Drive API
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open the Google Spreadsheet
spreadsheet = client.open_by_key(SHEET_ID)

# Get the source worksheet
source_worksheet = spreadsheet.worksheet(SOURCE_SHEET_NAME)

# Get the target worksheet
target_worksheet = spreadsheet.worksheet(TARGET_SHEET_NAME)

# Get all values in the 'email' column from the source worksheet
source_email_column_index = source_worksheet.find("email").col
source_emails = source_worksheet.col_values(source_email_column_index)

# Get all values in the 'email' column from the target worksheet
target_email_column_index = target_worksheet.find("email").col
target_emails = target_worksheet.col_values(target_email_column_index)

# Check if the 'email' column of the "1" sheet has the emails from the "Instantly" sheet
emails_in_both_sheets = set(source_emails).intersection(set(target_emails))

print(f"The following emails are present in both the '{SOURCE_SHEET_NAME}' and '{TARGET_SHEET_NAME}' sheets:")
for email in emails_in_both_sheets:
    print(email)

# Calculate and print the number of emails that are present in both sheets
num_emails_in_both_sheets = len(emails_in_both_sheets)
print(f"\nNumber of emails present in both sheets: {num_emails_in_both_sheets}")
