import datetime
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build
from tools.sheets_logger import log_booking

# complementary tool to book appt based on calendar availability and log info

# google calendar details
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'c_007b3759108ae41483c0489dd330450b3ef3691609cd3ff4133320820e19718c@group.calendar.google.com'
TIMEZONE = 'America/Los_Angeles'
SERVICE_ACCOUNT_FILE = 'credentials.json'

def get_calendar_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)

# check if appt wanted from user query is available in google calendar
def check_availability(service, date, time):
    tz = pytz.timezone(TIMEZONE)
    start_dt = tz.localize(datetime.datetime.combine(date, time))
    end_dt = start_dt + datetime.timedelta(minutes=30)

    body = {
        "timeMin": start_dt.isoformat(),
        "timeMax": end_dt.isoformat(),
        "timeZone": TIMEZONE,
        "items": [{"id": CALENDAR_ID}]
    }

    events_result = service.freebusy().query(body=body).execute()
    busy_slots = events_result['calendars'][CALENDAR_ID]['busy']
    return len(busy_slots) == 0

# if available, ask info and book which will save slot in calendar, log patient/appt info in google sheets, and generate link to gcal event
def book_appointment(service, name, email, date, time):
    if not check_availability(service, date, time):
        return None  # if slot already booked

    tz = pytz.timezone(TIMEZONE)
    start_dt = tz.localize(datetime.datetime.combine(date, time))
    end_dt = start_dt + datetime.timedelta(minutes=30)

    event = {
        'summary': f'Clinic Appointment - {name}',
        'description': f'Booked by {name}, email: {email}',
        'start': {
            'dateTime': start_dt.isoformat(),
            'timeZone': TIMEZONE,
        },
        'end': {
            'dateTime': end_dt.isoformat(),
            'timeZone': TIMEZONE,
        },
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

    # log info to sheets
    date_str = date.strftime('%Y-%m-%d')
    time_str = time.strftime('%I:%M %p')
    log_booking(name, email, date_str, time_str)
    return created_event.get('htmlLink')