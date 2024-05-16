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

def fetch_column_values():
    # Specified columns identified as empty
    columns = ['scraping_date', 'linkedin', 'twitter', 'personal_email', 'company_location_1', 'funding_events', 'total_funding']
    query_columns = ', '.join(columns)

    # Constructing the query
    query = f"""
        SELECT {query_columns}
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
        LIMIT 100  # Adjust the limit based on your needs
    """
    query_job = client.query(query)

    logging.info(f"Fetching values for columns: {', '.join(columns)}")
    for row in query_job:
        # Print out the row values; these are expected to be NULL based on previous checks
        print(row)

fetch_column_values()
