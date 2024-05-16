# drive_manager.py
from googleapiclient.errors import HttpError
import io
import logging

class DriveManager:
    def __init__(self, drive_service):
        self.service = drive_service

    def list_files(self, folder_id):
        try:
            results = self.service.files().list(
                q=f"'{folder_id}' in parents",
                fields="nextPageToken, files(id, name)").execute()
            return results.get('files', [])
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return []

    def download_file(self, file_id):
        try:
            request = self.service.files().get_media(fileId=file_id)
            file_io = io.BytesIO()
            downloader = MediaIoBaseDownload(file_io, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            file_io.seek(0)
            return file_io
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return None
