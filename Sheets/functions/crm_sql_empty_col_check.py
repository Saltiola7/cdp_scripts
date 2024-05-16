import logging
from google.cloud import bigquery
from google.oauth2 import service_account

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration for BigQuery
SERVICE_ACCOUNT_FILE = '/Users/tis/foam/cdp/code/cfg/Seotieto.json'
PROJECT_ID = 'seotieto'
DATASET_ID = 'crm'
TABLE_NAME = 'cold'

logging.info("Setting up credentials and client")

# Create credentials with Drive & BigQuery API scopes.
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/bigquery"],
)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

def verify_empty_columns():
    # List of columns to check
    empty_columns = ['scraping_date', 'linkedin', 'twitter', 'personal_email', 'company_location_1', 'funding_events', 'total_funding']
    
    for column in empty_columns:
        query = f"""
            SELECT COUNT(*) as non_null_count
            FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
            WHERE {column} IS NOT NULL
        """
        query_job = client.query(query)
        results = list(query_job)
        non_null_count = results[0].get("non_null_count")

        if non_null_count == 0:
            logging.info(f"Column '{column}' is confirmed to be completely empty.")
        else:
            logging.info(f"Column '{column}' is NOT completely empty. Non-null count: {non_null_count}")

verify_empty_columns()
