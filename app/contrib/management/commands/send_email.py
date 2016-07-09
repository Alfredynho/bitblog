# -*- encoding: utf-8 -*-
"""
Management command to send email using Django settings
"""
# Python imports
import os
import sys
from optparse import make_option

# Django imports
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.core.validators import validate_email

# Project imports
try:
    from django.utils.six.moves import input as raw_input
except ImportError:
    pass

CONFIRM_MESSAGE = '''
---------- MESSAGE FOLLOWS ----------
Subject: {subject}
From: {from_email}
To: {recipient_list_formatted}

{message}
------------ END MESSAGE ------------
'''


class Command(BaseCommand):
    pass