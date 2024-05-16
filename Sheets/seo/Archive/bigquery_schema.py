# schema.py

from google.cloud import bigquery

# Define schema for internal_all
SCHEMA_INTERNAL_ALL = [
    bigquery.SchemaField("Address", "STRING"),
    bigquery.SchemaField("Indexability", "STRING"),
    bigquery.SchemaField("Word_Count", "INTEGER"),
    bigquery.SchemaField("Title_1_Length", "INTEGER"),
    bigquery.SchemaField("Meta_Description_1_Length", "INTEGER"),
    bigquery.SchemaField("H1-1_Length", "INTEGER"),
    bigquery.SchemaField("H2-1_Length", "INTEGER"),
    bigquery.SchemaField("Title_1", "STRING"),
    bigquery.SchemaField("Meta_Description_1", "STRING"),
    bigquery.SchemaField("H1-1", "STRING"),
    bigquery.SchemaField("H1-2", "STRING"),
    bigquery.SchemaField("H1-2_Length", "INTEGER"),
    bigquery.SchemaField("H2-1", "STRING"),
    bigquery.SchemaField("H2-2", "STRING"),
    bigquery.SchemaField("H2-2_Length", "INTEGER"),
    bigquery.SchemaField("Status_Code", "INTEGER"),
    bigquery.SchemaField("Status", "STRING"),
    bigquery.SchemaField("Indexability_Status", "STRING"),
]

# Define schema for issues_overview_report
SCHEMA_ISSUES_OVERVIEW_REPORT = [
    bigquery.SchemaField("Issue_Name", "STRING"),
    bigquery.SchemaField("Issue_Type", "STRING"),
    bigquery.SchemaField("Issue_Priority", "STRING"),
    bigquery.SchemaField("URLs", "INTEGER"),
    bigquery.SchemaField("Description", "STRING"),
    bigquery.SchemaField("How_To_Fix", "STRING"),
]

# Define columns to upload for each schema
COLUMNS_TO_UPLOAD_INTERNAL_ALL = [field.name for field in SCHEMA_INTERNAL_ALL]
COLUMNS_TO_UPLOAD_ISSUES_OVERVIEW_REPORT = [field.name for field in SCHEMA_ISSUES_OVERVIEW_REPORT]