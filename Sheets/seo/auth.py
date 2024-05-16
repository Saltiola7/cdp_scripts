# auth.py
from google.cloud import storage, bigquery
from google.oauth2 import service_account

def get_authenticated_clients(service_account_file, project_id):
    credentials = service_account.Credentials.from_service_account_file(service_account_file)

    storage_client = storage.Client(credentials=credentials, project=project_id)
    bigquery_client = bigquery.Client(credentials=credentials, project=project_id)

    return storage_client, bigquery_client