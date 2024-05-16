# bigquery_manager.py
from google.cloud import bigquery
import pandas as pd
from data_sanitizer import sanitize_column_names

class BigQueryManager:
    def __init__(self, bigquery_client):
        self.client = bigquery_client

    def generate_schema(self, dataframe):
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

    def load_data_into_bigquery(self, dataframe, dataset_id, table_id, schema):
        table_ref = self.client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig(schema=schema, write_disposition='WRITE_TRUNCATE')
        job = self.client.load_table_from_dataframe(dataframe, table_ref, job_config=job_config)
        job.result()

    def execute_query(self, query):
        query_job = self.client.query(query)
        return query_job.result()
