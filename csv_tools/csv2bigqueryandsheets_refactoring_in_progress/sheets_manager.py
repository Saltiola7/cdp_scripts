# sheets_manager.py
from googleapiclient.errors import HttpError
import logging
import json

class SheetsManager:
    def __init__(self, sheets_service):
        self.service = sheets_service

    def create_sheet(self, title, folder_id):
        try:
            file_metadata = {
                'name': title,
                'mimeType': 'application/vnd.google-apps.spreadsheet',
                'parents': [folder_id]
            }
            file = self.service.files().create(body=file_metadata).execute()
            return file.get('id')
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return None

    def write_data_to_sheet(self, spreadsheet_id, sheet_name, data):
        try:
            body = {
                'values': data
            }
            range_ = f'{sheet_name}!A1'  # Starting at cell A1
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_,
                valueInputOption='RAW',
                body=body).execute()
            logging.info(f'Data written successfully to {sheet_name} in spreadsheet {spreadsheet_id}.')
        except HttpError as error:
            logging.error(f'An error occurred: {error}')

    def apply_conditional_rules(self, spreadsheet_id, sheet_name, conditional_formats):
        try:
            # Get the sheet ID of the target sheet
            sheet_ids = self.get_sheet_ids(spreadsheet_id)
            target_sheet_id = sheet_ids.get(sheet_name)

            # Create the requests for adding conditional formatting rules
            requests = []
            for rule in conditional_formats:
                if 'ranges' in rule and isinstance(rule['ranges'], list):
                    updated_rule = rule.copy()  # Create a copy of the rule to modify
                    updated_rule['ranges'] = [{
                        **range_info, 
                        'sheetId': target_sheet_id
                    } for range_info in rule['ranges']]
                    requests.append({"addConditionalFormatRule": {"rule": updated_rule, "index": 0}})
                else:
                    logging.warning(f"Rule does not have a 'ranges' or it's not a list: {json.dumps(rule)}")

            if requests:
                body = {'requests': requests}
                self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
                logging.info(f"Conditional formatting rules applied successfully to {sheet_name}.")
            else:
                logging.info(f"No valid conditional formatting rules found for {sheet_name}.")
        except HttpError as error:
            logging.error(f'An error occurred while applying conditional formatting: {error}')

    def get_sheet_ids(self, spreadsheet_id):
        try:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            return {sheet['properties']['title']: sheet['properties']['sheetId'] for sheet in sheets}
        except HttpError as error:
            logging.error(f'An error occurred: {error}')
            return {}

