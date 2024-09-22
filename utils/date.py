from datetime import datetime
import re

DATE_FORMAT = "%d/%m/%Y"

def is_date_format(new_value: str):
    # return true if format is DD/MM/YYYY
    return re.match(r'^\d{2}/\d{2}/\d{4}$', new_value)

def get_date_from_str(date: str):
    return datetime.strptime(date, DATE_FORMAT)

def get_period(start_date: datetime, end_date: datetime, unit_period: str):
    period_days = end_date - start_date

    if unit_period == 'months':
        return period_days.days / 30.44
    elif unit_period == 'years':
        return period_days.days / 365.25

    return period_days

def validate_and_generate_date(datestr: str):
    try:
        date = get_date_from_str(datestr)
        return (date, True)
    except:
        print("\nInvalid date! Please try again")
        return None, False
