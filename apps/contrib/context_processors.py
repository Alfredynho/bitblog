# -*- encoding: utf-8 -*-

from django.conf import settings


def website(request):
    """
    Returns common info about the website
    """
    return {
        'project_name': settings.PROJECT_NAME,
        'project_author': settings.PROJECT_AUTHOR,
        'DEBUG': settings.DEBUG,
    }