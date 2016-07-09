# -*- coding: utf-8 -*-

from .common import *
from os.path import dirname

import warnings

env = environ.Env()
env.read_env(join(dirname(PROJECT_DIR), "config/.environment"))


DEBUG = True
SECRET_KEY = env('SECRET_KEY', default='CHANGEME!!!')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
])

# MAIL
# ------------------------------------------------------------------------------
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Warpp <admin@warpp.xyz>')

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
    'RENDER_PANELS': True,
    'SHOW_COLLAPSED': True,
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]


INSTALLED_APPS += ('django_extensions', )
INTERNAL_IPS = ('127.0.0.1', '0.0.0.0', )
CORS_ORIGIN_ALLOW_ALL = True


DATABASES['default'] = env.db("DATABASE_URL")
CACHES["default"] = env.cache('REDIS_URL')


SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY', default='CHANGEME!!!')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET', default='CHANGEME!!!')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',

    'oauth.pipelines.get_avatar',
)

warnings.filterwarnings(
        'error', r"DateTimeField .* received a naive datetime",
        RuntimeWarning, r'django\.db\.models\.fields')