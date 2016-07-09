import datetime
import uuid

from django.conf import settings

import hashlib

from contrib.date import now, now_after


def compute_md5_hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def get_uuid():
    s = str(uuid.uuid4()).replace("-", "")
    return s.upper()


def get_lapse():
    now_date = now()
    end_date = now_after(days=settings.TOKEN_EXPIRATION_DAYS)

    return now_date, end_date


def get_hostname(request):
    if settings.MANAGE_TRANSACTIONS:
        if settings.USE_HTTPS:
            if 'HTTP_HOST' in request.META:
                return "https://"+request.META['HTTP_HOST']
            else:
                return settings.FRONTEND_URL.replace("http", "https")
        else:
            if 'HTTP_HOST' in request.META:
                return "http://"+request.META['HTTP_HOST']
            else:
                return settings.FRONTEND_URL
    else:
        return settings.FRONTEND_URL

