# config_manager.py
import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()

    @property
    def project_id(self):
        return os.getenv('PROJECT_ID')

    @property
    def dataset_id(self):
        return os.getenv('DATASET_ID')

    @property
    def service_account_file(self):
        return os.getenv('SERVICE_ACCOUNT_FILE')

    @property
    def drive_folder_id(self):
        return os.getenv('DRIVE_FOLDER_ID')

    @property
    def template_spreadsheet_id(self):
        return os.getenv('TEMPLATE_SPREADSHEET_ID')

    @property
    def spreadsheet_folder_id(self):
        return os.getenv('SPREADSHEET_FOLDER_ID')
