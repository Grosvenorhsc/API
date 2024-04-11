
from datetime import datetime

def parse_date(date_string, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    raise ValueError(f"time data {date_string} does not match any of the expected formats")

