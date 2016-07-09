# -*- encoding:utf-8 -*-

# Django imports
from django.conf import settings
from django.dispatch import Signal


# ------ Email------ #
EMAIL_CONFIRMATION = getattr(settings, 'PROFILE_EMAIL_CONFIRMATION', True)
REQUIRED_FIELDS = getattr(settings, 'PROFILE_REQUIRED_FIELDS', ['email'])
email_confirmed = Signal(providing_args=["email_address"])
email_confirmation_sent = Signal(providing_args=["confirmation"])

# ------ SIGNALS ------ #
user_logged_in = Signal(providing_args=["request", "user"])
password_changed = Signal(providing_args=["user", ])
user_cancel_account = Signal(providing_args=["user", "request_data"])

