# Import libraries
import io
import logging
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from drive_ops import get_drive_service, list_files_in_drive_folder, download_file_from_drive
load_dotenv('/Users/tis/foam/cdp/code/cfg/.env')


# Constants and configurations
PROJECT_ID = 'seotieto'
DATASET_ID = 'SEOTieto'
SERVICE_ACCOUNT_FILE = '/Users/tis/foam/cdp/function/seo/Seotieto.json'
DRIVE_FOLDER_ID = os.getenv('DRIVE_FOLDER_ID')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to sanitize column names

def sanitize_column_names(columns):
    return (
        columns
        .str.lower()  # convert to lowercase
        .str.replace(' ', '_')  # replace spaces with underscores
        .str.replace(r'[^\w\s]', '_', regex=True)
        .str.replace(r'__+', '_', regex=True)
        .str.strip('_')
        .str.replace(r'^(\d+)', r'_\1', regex=True)
    )
# Function to generate schema from pandas DataFrame
def generate_schema(dataframe):
    type_mapping = {
        'object': 'STRING',
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP'
    }
    schema = []
    for column_name, dtype in dataframe.dtypes.items():
        formatted_column_name = sanitize_column_names(pd.Series(column_name)).iloc[0]
        bq_type = type_mapping.get(str(dtype), 'STRING')  # Default to STRING if type not found
        schema.append(bigquery.SchemaField(formatted_column_name, bq_type))
    return schema

# Function to load data into BigQuery
def load_data_into_bigquery(bigquery_client, dataframe, dataset_id, table_id, schema):
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition='WRITE_TRUNCATE'
    )
    job = bigquery_client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
    job.result()
    logging.info(f"Data loaded into BigQuery table {dataset_id}.{table_id}")

# Main function
def main():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    bigquery_client = bigquery.Client(credentials=credentials, project=PROJECT_ID)
    drive_service = get_drive_service(SERVICE_ACCOUNT_FILE)
    
    drive_files = list_files_in_drive_folder(drive_service, DRIVE_FOLDER_ID)
    for file in drive_files:
        file_name = file['name']
        file_id = file['id']
        logging.info(f"Processing file: {file_name}")
        
        file_stream = download_file_from_drive(drive_service, file_id, file_name)
        file_stream.seek(0)
        df = pd.read_csv(file_stream)
        
        # Sanitize column names in the dataframe
        df.columns = sanitize_column_names(df.columns)
        
        # Generate schema based on the dataframe
        schema = generate_schema(df)
        table_id = file_name.split('.')[0]
        load_data_into_bigquery(bigquery_client, df, DATASET_ID, table_id, schema)
        
    logging.info("All files processed successfully.")

if __name__ == "__main__":
    main()
