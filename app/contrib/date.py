from datetime import datetime, timedelta
from django.utils.timezone import utc


def now():
    """ returns the current date and time in UTC format (datetime object) """
    return datetime.utcnow().replace(tzinfo=utc)


def now_after(**kwargs):
    """ returns the current date and time plus the time (seconds, minutes, hours, days, years) specified """
    return now() + timedelta(**kwargs)


def ago(**kwargs):
    """ returns the current date and time minus the time (seconds, minutes, hours, days, years) specified """
    return now() - timedelta(**kwargs)


def after(date, **kwargs):
    """
    returns the result of the calculation of the date param plus the time (seconds, minutes, hours, days, years) specified

    :paramm datetime: datetime object to which add more time
    """
    return date + timedelta(**kwargs)
