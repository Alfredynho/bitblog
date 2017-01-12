# -*- encoding:utf-8 -*-

import uuid

from django.conf import settings

import hashlib

from apps.contrib.format.date import now, now_after


def compute_md5_hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def get_uuid():
    s = str(uuid.uuid4()).replace("-", "")
    return s.upper()


def get_lapse():
    now_date = now()
    days = 7
    if settings.TOKEN_EXPIRATION_DAYS:
        days = settings.TOKEN_EXPIRATION_DAYS
    end_date = now_after(days=days)

    return now_date, end_date


def get_hostname(request):

    host = '127.0.0.1'
    if 'HTTP_HOST' in request.META:
        host = request.META['HTTP_HOST']

    if hasattr(settings, 'USE_HTTPS') and settings.USE_HTTPS:
        return "https://" + host
    else:
        return "http://" + host


