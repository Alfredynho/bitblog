import datetime
from django import template
from django.conf import settings

register = template.Library()


@register.assignment_tag
def project_domain():
    return settings["PROJECT_DOMAIN"]
