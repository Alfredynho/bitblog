# -*- encoding:utf-8 -*-

from django.apps import AppConfig


class CredentialsConfig(AppConfig):
    name = 'apps.credentials'
    verbose_name = "Credentials"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
