import pandas as pd
import json
from google.cloud import bigquery
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Provide the path to your service account key file
key_path = "/Users/tis/Dendron/notes/SEOTieto/Seotieto.json"

# Initialize the BigQuery, Sheets and Drive API
credentials = Credentials.from_service_account_file(key_path, scopes=[
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
])
client = bigquery.Client(credentials=credentials, project=credentials.project_id)
sheets_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

# Retrieve brand names from BigQuery
query = """
SELECT 
    SUBSTR(table_name, 0, STRPOS(table_name, '_') - 1) AS brand_name
FROM 
    `seotieto.SEOTieto.INFORMATION_SCHEMA.TABLES`
WHERE 
    table_name LIKE '%_internal_all%'
"""
query_job = client.query(query)
brand_names = {row["brand_name"] for row in query_job}
logging.info(f"Retrieved brand names: {brand_names}")

# Function to retrieve data for a brand
def get_data_for_brand(brand):
    df1_query = f"""
    SELECT
        address,
        word_count AS words,
        title_1_length,
        meta_description_1_length AS meta_length,
        title_1,
        meta_description_1 AS meta
    FROM `seotieto.SEOTieto.{brand}_internal_all`
    WHERE content_type IN (
        'text/html; charset=utf-8',
        'text/html;charset=UTF-8',
        'text/html; charset=iso-8859-1',
        'text/html;charset=utf-8',
        'text/html',
        'text/html; charset=UTF-8'
    )
    AND status_code = 200
    AND indexability = "Indexable"
    """
    df2_query = f"""
    SELECT
        issue_name AS name,
        issue_type AS type,
        issue_priority AS priority,
        urls,
        description,
        how_to_fix AS fix
    FROM `seotieto.SEOTieto.{brand}_issues_overview_report`
    WHERE issue_name NOT IN (
        'Security: Missing X-Content-Type-Options Header',
        'Security: Missing X-Frame-Options Header',
        'Security: Missing HSTS Header',
        'Security: Missing Content-Security-Policy Header',
        'Security: Protocol-Relative Resource Links',
        'Security: Unsafe Cross-Origin Links',
        'Links: Pages With High External Outlinks',
        'Links: Internal Outlinks With No Anchor Text',
        'Content: Readability Very Difficult',
        'Security: Bad Content Type',
        'Page Titles: Over 561 Pixels',
        'Page Titles: Below 200 Pixels',
        'Response Codes: Internal Redirection (3xx)',
        'Directives: Noindex',
        'URL: Underscores',
        'URL: Parameters',
        'Directives: Nofollow',
        'Canonicals: Canonicalised',
        'Canonicals: Missing',
        'Security: HTTP URLs',
        'Pagination: Sequence Error',
        'Response Codes: External Client Error (4xx)',
        'Content: Readability Difficult',
        'Meta Description: Below 400 Pixels',
        'Meta Description: Below 400 Pixels'
    )
    ORDER BY issue_name ASC, urls DESC
    """
    
    df1 = client.query(df1_query).result().to_dataframe()
    df2 = client.query(df2_query).result().to_dataframe()
    
    return df1, df2

# Fetch and prepare conditional formatting rules
SHEET_ID = '1gv6fvbppsceqD55InoHg85gsOjR5wA_9Vjc-vnPvG2g'
SHEET_NAMES = ['internal_extract', 'issues_extract']
sheet_metadata = sheets_service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
sheets = sheet_metadata.get('sheets', '')
sheet_ids = {sheet['properties']['title']: sheet['properties']['sheetId'] for sheet in sheets if sheet['properties']['title'] in SHEET_NAMES}
conditional_formats = {
    sheet_name: sheets_service.spreadsheets().get(
        spreadsheetId=SHEET_ID, ranges=sheet_name, fields='sheets(conditionalFormats)'
    ).execute().get('sheets', [])[0].get('conditionalFormats', [])
    for sheet_name in sheet_ids.keys()
}

# Function to create and populate a new Google Sheet for each brand
def create_and_populate_sheet(brand, df1, df2, folder_id='12xrF81B81UORxXtKGul6GT19gpkZmt1l'):
    try:
        # Create new Google Sheet
        sheet_metadata = {
            'properties': {'title': brand},
            'sheets': [{'properties': {'title': 'internal'}}, {'properties': {'title': 'issues'}}]
        }
        sheet = drive_service.files().create(body=sheet_metadata, fields='id').execute()
        spreadsheet_id = sheet.get('id')

        # Move the spreadsheet to the specified folder
        drive_service.files().update(fileId=spreadsheet_id,
                                     addParents=folder_id,
                                     removeParents='root',
                                     fields='id, parents').execute()

        # Prepare data for batchUpdate
        data = [
            {
                'range': 'internal!A1',
                'values': df1.values.tolist()
            },
            {
                'range': 'issues!A1',
                'values': df2.values.tolist()
            }
        ]
        body = {
            'valueInputOption': 'RAW',
            'data': data
        }
        sheets_service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        # Apply conditional formatting rules
        requests = []
        for sheet_name, formats in conditional_formats.items():
            for format_rule in formats:
                format_rule['ranges'][0]['sheetId'] = sheet_ids[sheet_name]
                requests.append({'addConditionalFormatRule': {'rule': format_rule, 'index': 0}})
        
        body = {'requests': requests}
        sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        logging.info(f'Sheet created and populated for {brand} with ID {spreadsheet_id}')
    except Exception as e:
        logging.error(f'Error creating sheet for {brand}: {e}')

# Retrieve data for each brand and create sheets
for brand in brand_names:
    df1, df2 = get_data_for_brand(brand)
    create_and_populate_sheet(brand, df1, df2)

logging.info('Script completed.')
