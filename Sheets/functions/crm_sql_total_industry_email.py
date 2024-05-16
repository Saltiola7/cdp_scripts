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

def fetch_records():
    # Constructing the query
    query = f"""
        SELECT COUNT(*)
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
        WHERE scraping_notes = 'altmed-us-canada' AND email IS NOT NULL
    """
    query_job = client.query(query)

    logging.info("Fetching the count of records where scraping_notes is 'altmed-us-canada' and email is not empty")
    for row in query_job:
        # Print out the count
        print(f"Count of records: {row[0]}")

fetch_records()
