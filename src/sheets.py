import os
from datetime import datetime

import gspread
from dotenv import load_dotenv


load_dotenv('config/.env')


class SheetAccount:
    """Google API account for Google Sheets."""

    credentials = {
        'type': 'service_account',
        'project_id': os.environ['GOOGLE_PROJECT_ID'],
        'private_key_id': os.environ['GOOGLE_PRIVATE_KEY_ID'],
        'private_key': os.environ['GOOGLE_PRIVATE_KEY'].replace('\\n', '\n'),
        'client_email': os.environ['GOOGLE_CLIENT_EMAIL'],
        'client_id': os.environ['GOOGLE_CLIENT_ID'],
        'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
        'token_uri': 'https://oauth2.googleapis.com/token',
        'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
        'client_x509_cert_url': os.environ['GOOGLE_CLIENT_X509_CERT_URL']
    }
    sheet_name = os.environ['GOOGLE_SHEET_NAME']

    def __init__(self):
        self.account = gspread.service_account_from_dict(self.credentials)
        self.sheet = self.account.open(self.sheet_name).sheet1

    def save_answer(self,
                    time: datetime,
                    user_id: int,
                    user_name: str,
                    text: str) -> None:
        # Unique user check.
        records = self.sheet.get_all_records()
        for i, record in enumerate(records, start=2):
            if str(record.get('User ID')) == str(user_id):
                raise ValueError(f'User {user_id} already exists in the sheet.')

        row_data = [
            time.strftime('%Y-%m-%d %H:%M:%S'),
            user_id,
            f'@{user_name}' if user_name else '',
            text,
        ]
        self.sheet.append_row(row_data)
