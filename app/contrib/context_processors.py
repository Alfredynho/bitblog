# -*- encoding: utf-8 -*-

from django.conf import settings


def website(request):
    """
    Returns common info about the website
    """
    return {
        'website_name': settings.WEBSITE_NAME,
        'website_author': settings.WEBSITE_AUTHOR,
        'DEBUG': settings.DEBUG,
    }