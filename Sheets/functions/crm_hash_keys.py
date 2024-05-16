import hashlib
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Configuration
SERVICE_ACCOUNT_FILE = '/Users/tis/foam/cdp/code/cfg/Seotieto.json'
SHEET_ID = 'SHEET_ID'
RANGE_NAME = '1'  # Replace 'YourSheetName' with your actual sheet name
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_google_sheets():
    """Authenticate with the Google Sheets API using a service account."""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()

def get_sheet_data(spreadsheet_id, range_name):
    """Retrieve data from a specified range in a Google Sheet."""
    service = authenticate_google_sheets()
    result = service.values().get(spreadsheetId=spreadsheet_id, range=range_name, majorDimension='ROWS').execute()
    return result.get('values', [])

def generate_hash(fields_to_hash):
    """Generates a SHA-256 hash from the given list of fields."""
    hash_input = ''.join(fields_to_hash)
    return hashlib.sha256(hash_input.encode()).hexdigest()

def update_key_column(spreadsheet_id, updates):
    """Update the 'key' column in the Google Sheet with new hash values."""
    service = authenticate_google_sheets()
    body = {
        "valueInputOption": "RAW",
        "data": updates
    }
    service.values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

def find_column_indices(header_row):
    """Find indices of required columns by name."""
    indices = {name: header_row.index(name) for name in ['key', 'full_name', 'first_name', 'last_name', 'scraping_notes'] if name in header_row}
    return indices

def main():
    data = get_sheet_data(SHEET_ID, RANGE_NAME)
    if not data:
        print("No data found.")
        return

    headers, rows = data[0], data[1:]
    col_indices = find_column_indices(headers)
    updates = []

    for i, row in enumerate(rows, start=2):  # Start from 2 because Google Sheets is 1-indexed and headers are in the first row
        row_data = [row[col_indices[col]] if col in col_indices and len(row) > col_indices[col] else '' for col in ['full_name', 'first_name', 'last_name', 'scraping_notes']]
        
        # Check if at least scraping_notes + one more field exists and key is empty
        if len([d for d in row_data[:-1] if d]) >= 1 and row_data[-1] and (not row[col_indices['key']] if 'key' in col_indices and len(row) > col_indices['key'] else True):
            hash_value = generate_hash(row_data)
            updates.append({
                "range": f"{RANGE_NAME}!{chr(65 + col_indices['key'])}{i}",
                "values": [[hash_value]]
            })

    if updates:
        update_key_column(SHEET_ID, updates)
        print(f"Updated {len(updates)} 'key' cells.")
    else:
        print("No 'key' cells required updates.")

if __name__ == '__main__':
    main()
