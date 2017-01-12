# -*- coding: utf-8 -*-

from django.conf import settings
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives

from apps.contrib.format.strings import get_hostname


def make_context(request, user=None, path=None):
    hostname = get_hostname(request)
    data = dict()
    if path:
        data["host"] = hostname + path
    if user:
        data["user"] = user
    return RequestContext(request=request, dict_=data)


def send_email(subject, to, text_body, html_body):

    email = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to, body=text_body,
    )

    email.attach_alternative(html_body, "text/html")
    email.send()
