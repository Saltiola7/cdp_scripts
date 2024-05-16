# main.py
import logging
import io
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from drive_ops import get_drive_service, list_files_in_drive_folder, download_file_from_drive
from bigquery_ops import create_table_if_not_exists, load_data_into_bigquery
from code.function.seo.Archive.bigquery_schema import SCHEMA_ISSUES_OVERVIEW_REPORT, SCHEMA_INTERNAL_ALL, COLUMNS_TO_UPLOAD_ISSUES_OVERVIEW_REPORT, COLUMNS_TO_UPLOAD_INTERNAL_ALL
from dotenv import load_dotenv
load_dotenv('/Users/tis/foam/cdp/code/cfg/.env')
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Define your Google Cloud project details
        project_id = 'seotieto'
        dataset_id = 'SEOTieto'
        service_account_file = '/Users/tis/foam/cdp/code/cfg/Seotieto.json'
        drive_folder_id = os.getenv('DRIVE_FOLDER_ID')

        # Get credentials from service account file
        credentials = service_account.Credentials.from_service_account_file(service_account_file)

        # Get authenticated clients
        bigquery_client = bigquery.Client(credentials=credentials, project=project_id)
        drive_service = get_drive_service(service_account_file)

        # List and process files in the Google Drive folder
        drive_files = list_files_in_drive_folder(drive_service, drive_folder_id)
        for file in drive_files:
            file_name = file['name']
            file_id = file['id']
            logging.info(f"Processing file: {file_name}")

            # Download the file
            file_stream = download_file_from_drive(drive_service, file_id, file_name)
            
            # Convert the file stream to pandas DataFrame
            file_stream.seek(0)  # Move to the beginning of the file
            df = pd.read_csv(file_stream)
            df.columns = df.columns.str.replace(' ', '_', regex=False)  # Replace spaces with underscores
            
            # Determine the columns to upload based on the file name
            if 'issues_overview_report' in file_name:
                columns_to_upload = COLUMNS_TO_UPLOAD_ISSUES_OVERVIEW_REPORT
            elif 'internal_all' in file_name:
                columns_to_upload = COLUMNS_TO_UPLOAD_INTERNAL_ALL
            else:
                logging.error(f"Unknown file: {file_name}")
                continue  # Skip this file if it doesn't match known patterns
            
            # Select only the columns that exist in the DataFrame and are also in columns_to_upload
            df = df[df.columns.intersection(columns_to_upload)]
            
            # Process file for BigQuery
            process_file(bigquery_client, dataset_id, file_name, df)

        logging.info("All files processed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

def process_file(bigquery_client, dataset_id, file_name, df):
    try:
        table_id = file_name.split('.')[0]
        table_ref = bigquery_client.dataset(dataset_id).table(table_id)

        # Determine the schema based on the file name
        if 'issues_overview_report' in file_name:
            schema = SCHEMA_ISSUES_OVERVIEW_REPORT
        elif 'internal_all' in file_name:
            schema = SCHEMA_INTERNAL_ALL
        else:
            logging.error(f"Unknown file: {file_name}")
            return

        # Filter the schema based on columns present in the DataFrame
        schema = [field for field in schema if field.name in df.columns]

        # Check if table already exists
        try:
            bigquery_client.get_table(table_ref)
            print(f"Table {table_id} already exists.")
        except NotFound:
            # Create the table with the defined schema if it does not exist
            create_table_if_not_exists(bigquery_client, dataset_id, table_id, schema)
            print(f"Table {table_id} does not exist.")

        # Save DataFrame to CSV (can be commented out if not needed)
        # df.to_csv(f"{table_id}_for_bigquery.csv", index=False)  # Uncomment this line to save the DataFrame as CSV

        # Load the DataFrame into BigQuery using the filtered schema
        load_data_into_bigquery(bigquery_client, df, dataset_id, table_id, schema, autodetect=False)
        print(f"Data loaded into BigQuery table {table_id}.")
    except Exception as e:
        logging.error(f"Error in processing file {file_name}: {e}")
        raise

if __name__ == "__main__":
    main()
