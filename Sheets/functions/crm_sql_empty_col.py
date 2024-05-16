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
# Construct a BigQuery client object.
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

logging.info("Credentials and client setup complete")

def fetch_column_names():
    logging.info(f"Fetching column names for table: {PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}")
    query = f"""
        SELECT column_name
        FROM `{PROJECT_ID}.{DATASET_ID}.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = '{TABLE_NAME}'
    """
    query_job = client.query(query)
    return [row["column_name"] for row in query_job]

def check_empty_columns():
    columns = fetch_column_names()
    logging.info(f"Checking for empty columns in: {TABLE_NAME}")

    # Construct a CASE statement for each column to check for non-null values
    case_statements = [f"MAX(CASE WHEN {col} IS NOT NULL THEN 1 ELSE 0 END) AS {col}" for col in columns]
    query = f"""
        SELECT {', '.join(case_statements)}
        FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
    """
    query_job = client.query(query)
    results = list(query_job)[0]  # Assuming the query returns a single row

    # Identify columns where the max case statement returned 0, indicating all values are NULL
    empty_columns = [col for col, value in results.items() if value == 0]

    if empty_columns:
        logging.info(f"Empty columns: {', '.join(empty_columns)}")
        print("Empty columns:", ", ".join(empty_columns))
    else:
        logging.info("No empty columns found.")
        print("No empty columns found.")

# Execute the optimized function
check_empty_columns()
