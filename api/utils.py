from datetime import datetime


def to_date(str_date, date_format="%Y-%m-%d"):
    if not str_date:
        return None
    try:
        return datetime.strptime(str_date, date_format).date()
    except:
        return None
