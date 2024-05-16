# delete_tables.py
from auth import get_authenticated_clients

# Specify your service account file and project ID
service_account_file = '/Users/tis/Dendron/notes/SEOTieto/Seotieto.json'
project_id = 'seotieto'

# Get authenticated clients
storage_client, bigquery_client = get_authenticated_clients(service_account_file, project_id)

# Specify your dataset
dataset_id = 'SEOTieto'

# List all the tables in the dataset
tables = bigquery_client.list_tables(dataset_id)

# Loop through each table and delete it
for table in tables:
    table_id = f"{dataset_id}.{table.table_id}"
    bigquery_client.delete_table(table_id, not_found_ok=True)  # Make an API request.
    print(f"Deleted table '{table_id}'")