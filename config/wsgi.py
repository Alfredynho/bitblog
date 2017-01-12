# -*- encoding:utf-8 -*-

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")


application = get_wsgi_application()

# from django.core.wsgi import get_wsgi_application
# if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':

# from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.production"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# application = get_wsgi_application()
# if os.environ.get('DJANGO_SETTINGS_MODULE') == 'config.settings.production':
#     application = Sentry(application)





