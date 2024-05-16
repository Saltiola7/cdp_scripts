# main.py
from config_manager import ConfigManager
from auth_manager import AuthManager
from bigquery_manager import BigQueryManager
from drive_manager import DriveManager
from sheets_manager import SheetsManager
from data_sanitizer import sanitize_column_names
from data_loader import DataLoader
from query_builder import QueryBuilder
from logging_manager import configure_logging

def main():
    configure_logging()
    config = ConfigManager()
    auth = AuthManager(config.service_account_file)

    bigquery_client = auth.get_bigquery_client()
    sheets_service = auth.get_sheets_service()
    drive_service = auth.get_drive_service()

    bq_manager = BigQueryManager(bigquery_client)
    drive_manager = DriveManager(drive_service)
    sheets_manager = SheetsManager(sheets_service)
    data_loader = DataLoader()
    query_builder = QueryBuilder(bigquery_client)

    # Load and process files from Drive
    drive_files = drive_manager.list_files(config.drive_folder_id)
    for file in drive_files:
        file_name = file['name']
        file_id = file['id']
        file_stream = drive_manager.download_file(file_id)
        df = data_loader.load_csv(file_stream)
        df.columns = sanitize_column_names(df.columns)

        # Generate schema based on the dataframe and load data into BigQuery
        schema = bq_manager.generate_schema(df)
        table_id = file_name.split('.')[0]
        bq_manager.load_data_into_bigquery(df, config.dataset_id, table_id, schema)

    # Fetch brand names from BigQuery for further processing
    brand_names_query = """
    SELECT SUBSTR(table_name, 0, STRPOS(table_name, '_') - 1) AS brand_name
    FROM `{}.{}.INFORMATION_SCHEMA.TABLES`
    WHERE table_name LIKE '%_internal_all%'
    """.format(config.project_id, config.dataset_id)
    brand_names_result = query_builder.execute_query(brand_names_query)
    brand_names = {row["brand_name"] for row in brand_names_result}

    for brand in brand_names:
        # Fetch and process data for each brand, create sheets, and apply formatting
        pass  # Detailed processing logic and sheet creation goes here

if __name__ == "__main__":
    main()
