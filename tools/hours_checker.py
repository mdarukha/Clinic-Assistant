import re
from datetime import datetime, timedelta

# tool to parse user query for day and time, and return info about clinic being open or closed based on clinic hours

# sample clinic hours, closed on weekends
CLINIC_HOURS = {
    "monday":    (8, 18),
    "tuesday":   (8, 18),
    "wednesday": (8, 18),
    "thursday":  (8, 18),
    "friday":    (8, 18),
    "saturday":  None,  
    "sunday":    None, 
}

# returns datetime object for next occurence of target weekday
def get_next_weekday(target_weekday):
    today = datetime.now()
    days_ahead = (target_weekday - today.weekday() + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    return today + timedelta(days=days_ahead)

# parses query for day and time
def parse_day_and_time(query):
    query = query.lower()
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # extract day
    day = next((d for d in weekdays if d in query), None)

    # extract time
    time_match = re.search(r"(\d{1,2})(:(\d{2}))?\s*(am|pm)?", query)
    hour = None

    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(3)) if time_match.group(3) else 0
        meridian = time_match.group(4)

        if meridian:
            if meridian.lower() == "pm" and hour != 12:
                hour += 12
            elif meridian.lower() == "am" and hour == 12:
                hour = 0

    return day, hour

# responds to queries regarding clinic hours
def check_hours(query):
    day, hour = parse_day_and_time(query)

    if not day:
        return "Our hours are Monday to Friday 8 AM – 6 PM. We are closed on weekends."

    open_hours = CLINIC_HOURS.get(day)

    if open_hours is None:
        return f"We are closed on {day.capitalize()}s."

    open_hr, close_hr = open_hours

    if hour is None:
        return f"Yes, we are open on {day.capitalize()}s from {open_hr}:00 to {close_hr}:00."

    # check if clinic is open at that time
    if open_hr <= hour < close_hr:
        return f"Yes, we are open on {day.capitalize()}s at that time."
    else:
        return f"Sorry, we are closed on {day.capitalize()}s at that time. Our hours are {open_hr}:00 to {close_hr}:00."