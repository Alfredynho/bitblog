"""
WSGI
"""
# import os


# from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise

# if os.environ.get("DJANGO_SETTINGS_MODULE") == "settings.production":
    # from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "settings.production"
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

# This application object is used by any WSGI server red to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
# application = get_wsgi_application()

# Use Whitenoise to serve static files
# See: https://whitenoise.readthedocs.org/
# application = DjangoWhiteNoise(application)
# if os.environ.get("DJANGO_SETTINGS_MODULE") == "settings.production":
#     application = Sentry(application)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()






