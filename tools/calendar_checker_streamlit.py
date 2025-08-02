import pytz
import sys
from datetime import datetime, timedelta
from dateutil import parser as dtparser
from tools.gcal_scheduler import get_calendar_service, check_availability, book_appointment
from tools.sheets_logger import log_booking

# mostly same as one used for CLI but main different using status messages when check/book appt since streamlit doesn't accept input()

TIMEZONE = 'America/Los_Angeles'
CLINIC_OPEN_HOUR = 8
CLINIC_CLOSE_HOUR = 18

def is_cli():
    return sys.stdin.isatty()

def is_within_business_hours(date: datetime.date, time: datetime.time) -> bool:
    weekday = date.weekday()  # 0 = Monday
    return weekday < 5 and CLINIC_OPEN_HOUR <= time.hour < CLINIC_CLOSE_HOUR

def round_up_to_next_half_hour(dt):
    if dt.minute == 0 and dt.second == 0:
        return dt.replace(second=0, microsecond=0)
    else:
        minutes = 30 - (dt.minute % 30)
        return (dt + timedelta(minutes=minutes)).replace(second=0, microsecond=0)

def find_next_available_slot(service, start_date=None, start_time=None):
    timezone = pytz.timezone(TIMEZONE)

    if not start_date or not start_time:
        now = datetime.now(timezone) + timedelta(minutes=1)
        current = round_up_to_next_half_hour(now)
    else:
        combined = datetime.combine(start_date, start_time)
        localized = timezone.localize(combined)
        current = round_up_to_next_half_hour(localized)

    for _ in range(30 * 24 * 2):
        if CLINIC_OPEN_HOUR <= current.hour < CLINIC_CLOSE_HOUR:
            if check_availability(service, current.date(), current.time()):
                return current.date(), current.time()
        current += timedelta(minutes=30)

    return None, None

def check_and_book_appointment(query, name=None, email=None, confirm=None):
    service = get_calendar_service()

    try:
        dt = dtparser.parse(query, fuzzy=True)
        date = dt.date()
        time = dt.time()
    except Exception:
        next_date, next_time = find_next_available_slot(service)
        if next_date:
            return {
                "status": "done",
                "message": f"The next available appointment is at {next_time.strftime('%I:%M %p')} on {next_date.strftime('%A, %B %d')}."
            }
        else:
            return {
                "status": "done",
                "message": "Sorry, I couldn't find any open slots in the coming days."
            }

    if not is_within_business_hours(date, time):
        return {
            "status": "done",
            "message": "Our clinic only accepts appointments Monday to Friday between 9 AM and 5 PM. Please try a time during business hours."
        }

    if not check_availability(service, date, time):
        next_date, next_time = find_next_available_slot(service, date, time)
        if next_date:
            return {
                "status": "done",
                "message": f"Sorry, that time is already booked. The next available slot is {next_time.strftime('%I:%M %p')} on {next_date.strftime('%A, %B %d')}."
            }
        else:
            return {
                "status": "done",
                "message": "That time is booked, and no slots are available in the next few days."
            }

    # prompt for missing info sequentially
    if not name:
        return {"status": "need_name", "message": "What's your name?"}
    if not email:
        return {"status": "need_email", "message": "What's your email?"}
    if not confirm or confirm.lower() != "confirm":
        return {"status": "need_confirm", "message": "Type 'confirm' to finalize booking."}

    # book appointment
    event_link = book_appointment(service, name, email, date, time)
    log_booking(name, email, date.strftime('%Y-%m-%d'), time.strftime('%H:%M'))

    return {
        "status": "done",
        "message": f"Booking confirmed for {name} at {time.strftime('%I:%M %p')} on {date.strftime('%A, %B %d')}.\n🔗 Event: {event_link}"
    }