from google.oauth2 import service_account
from googleapiclient.discovery import build

# tool to log patient/appt info to integrated google sheets

# google sheets details
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1w9xGWFnCSdQ7i70cw8eEbQMeYmF4YNG7Wj8V-ir3FCE' 
SHEET_NAME = 'Bookings'

# service account credentials
def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=SCOPES
    )
    return build('sheets', 'v4', credentials=credentials)

# log patient/appt booking info: name, email, date/time of appt
def log_booking(name, email, date_str, time_str):
    service = get_sheets_service()
    sheet = service.spreadsheets()
    values = [[name, email, date_str, time_str]]
    body = {
        'values': values
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A:D',
        valueInputOption='RAW',
        body=body
    ).execute()
    return result.get('updates', {}).get('updatedCells', 0)