# auth_manager.py
from google.oauth2.service_account import Credentials
from google.cloud import bigquery
from googleapiclient.discovery import build

class AuthManager:
    def __init__(self, service_account_file):
        self.credentials = self._get_credentials(service_account_file)

    def _get_credentials(self, service_account_file):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
                  'https://www.googleapis.com/auth/drive']
        return Credentials.from_service_account_file(service_account_file, scopes=SCOPES)

    def get_bigquery_client(self):
        return bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)

    def get_sheets_service(self):
        return build('sheets', 'v4', credentials=self.credentials)

    def get_drive_service(self):
        return build('drive', 'v3', credentials=self.credentials)
