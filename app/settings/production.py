# -*- coding: utf-8 -*-
"""
Production Configurations
"""

from .common import *
env = environ.Env()
env.read_env(join(dirname(PROJECT_DIR), "config/.environment"))


DEBUG = False
INSTALLED_APPS += ("anymail",)


DATABASES['default'] = env.db("DATABASE_URL")
CACHES["default"] = env.cache('REDIS_URL')


# CELERY
# INSTALLED_APPS += ('taskapp.celery.CeleryConfig',)

# BROKER_URL = env("CELERY_BROKER_URL", default='django://')
# THUMBNAILING
# THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.dbm_kvstore.KVStore"
# THUMBNAIL_DBM_FILE = join(dirname(PROJECT_DIR), 'cache/sorl_cache')
# THUMBNAIL_CACHE_TIMEOUT = 3600 * 24 * 365 * 10
# IMPORT / EXPORT
# IMPORT_EXPORT_TMP_STORAGE_CLASS = 'referendum.storages.Utf8TempFolderStorage'


# EMAIL CONFIGURATION
# ANYMAIL = {
#     "MAILGUN_API_KEY": env('MAILGUN_API_KEY', default='CHANGEME!!!'),
#     "MAILGUN_SEND_DEFAULTS": {
#         "esp_extra": {"sender_domain": "xiberty.com"}
#     }
# }

EMAIL_HOST, EMAIL_PORT = 'localhost', 25  # Work with MailHog
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"  # or sendgrid.SendGridBackend, or...

DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Warpp <hello@victoraguilar.net>')


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
])


CORS_ORIGIN_ALLOW_ALL = True
# THUMBNAIL_KVSTORE = "sorl.thumbnail.kvstores.cached_db_kvstore.KVStore"

COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
]

COMPRESS_ENABLED = False
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'
COMPRESS_REBUILD_TIMEOUT = 86400


