# bigquery_ops.py
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import os
import pandas as pd

def create_table_if_not_exists(bigquery_client, dataset_id, table_id, schema):
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    table = bigquery.Table(table_ref, schema=schema)
    try:
        bigquery_client.get_table(table_ref)  # Make an API request.
        print(f"Table {table_id} already exists.")
    except NotFound:
        table = bigquery_client.create_table(table)  # API request.
        print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}.")

def clean_and_save_csv(dataframe, table_id, schema):
    # Ensure all schema columns are present in the DataFrame
    for field in schema:
        if field.name not in dataframe.columns:
            if field.field_type == 'STRING':
                dataframe[field.name] = ''  # Fill missing string columns with empty string
            elif field.field_type == 'INTEGER':
                dataframe[field.name] = 0   # Fill missing integer columns with 0
            # Add more conditions here for other data types as necessary
    
    # Replace spaces with underscores in DataFrame column names to match BigQuery schema
    dataframe.columns = dataframe.columns.str.replace(' ', '_', regex=False)
    
    # Define the CSV file path
    csv_export_dir = 'csv_exports'
    if not os.path.exists(csv_export_dir):
        os.makedirs(csv_export_dir)
    csv_file_path = os.path.join(csv_export_dir, f"{table_id}.csv")
    
    # Save the DataFrame to a CSV file
    dataframe.to_csv(csv_file_path, index=False)
    print(f"DataFrame cleaned and saved as CSV to {csv_file_path}")

    # Return the CSV file path
    return csv_file_path

def load_data_into_bigquery(bigquery_client, file_path_or_dataframe, dataset_id, table_id, schema, autodetect=True):
    table_ref = bigquery_client.dataset(dataset_id).table(table_id)
    
    # Define job configuration
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        autodetect=autodetect,
        write_disposition='WRITE_TRUNCATE'  # Overwrites the table. Use WRITE_APPEND to append data.
    )

    # Check if file_path_or_dataframe is a DataFrame or a file path
    if isinstance(file_path_or_dataframe, pd.DataFrame):
        # Clean the DataFrame and save it as CSV
        dataframe = file_path_or_dataframe
        clean_and_save_csv(dataframe, table_id, schema)
    else:
        # Assume file_path_or_dataframe is a file path
        dataframe = pd.read_csv(file_path_or_dataframe)

    # Load the data from the DataFrame into BigQuery
    job = bigquery_client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)

    # Wait for the load job to complete
    job.result()
    print(f"Data loaded into BigQuery table {dataset_id}.{table_id}")