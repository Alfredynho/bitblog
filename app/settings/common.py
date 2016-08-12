# -*- coding: utf-8 -*-
"""
Django settings for Warpp project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals
from os.path import join, dirname
import environ


env = environ.Env()
PROJECT_DIR = dirname(dirname(__file__))

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
DEBUG = env('DEBUG', default=False)
SECRET_KEY = env('SECRET_KEY', default='CHANGEME!!!')


# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Admin
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',
)

THIRD_PARTY_APPS = (
    # Admin
    # 'sorl.thumbnail',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailsites',
    'wagtail.wagtailredirects',
    'wagtail.wagtailforms',
    'wagtail.contrib.wagtailsitemaps',
    'wagtail.contrib.wagtailroutablepage',
    'compressor',
    'taggit',
    'modelcluster',

    # Templating
    'overextends',
    'import_export',

    # Authentication
    'oauth2_provider',
    'social.apps.django_app.default',

    # API Rest
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',
    'wagalytics',
    'wagtailfontawesome',

)

# Apps specific for this project go here.
LOCAL_APPS = (
    'contrib',
    'users',
    'oauth',
    'blog',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    # 'sites': 'contrib.sites.migrations',
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (
    join(PROJECT_DIR, 'fixtures'),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST, EMAIL_PORT = '127.0.0.1', 1025  # Work with MailHog
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Warpp <admin@warpp.xyz>')


# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("Admin", 'admin@warpp.xyz'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': env.db("DATABASE_URL", default="sqlite://%s" % dirname(PROJECT_DIR) + '/development.db'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'
# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'es'
# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(PROJECT_DIR, 'templates'),
        ],
        'OPTIONS': {
            'debug': True,
            'loaders': [
                'admin_tools.template_loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',

                # Your stuff: custom template context processors go here
                'contrib.context_processors.website',
                'django.core.context_processors.request',
            ],
            # To override template from third part apps
            'builtins': ['overextends.templatetags.overextends_tags'],
        },
    },
]


# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------

STATIC_ROOT = join(dirname(PROJECT_DIR), 'public/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    join(PROJECT_DIR, 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------

MEDIA_ROOT = join(dirname(PROJECT_DIR), 'public/media')
MEDIA_URL = '/media/'


# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'urls'
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'


# LOGGING SETTINGS
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '%s/django.log' % join(dirname(PROJECT_DIR), 'var/log'),
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            # 'handlers': ['mail_admins'],
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------

AUTHENTICATION_BACKENDS = (
    # OpenID
    'social.backends.open_id.OpenIdAuth',

    # Facebook OAuth2
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',

    # OWN oauth
    'oauth.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

AUTH_USER_MODEL = 'users.User'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

ADMIN_URL = r'^admin/'

# Swagger Docs Config
SWAGGER_SETTINGS = {
    'info': {
        'contact': env('DEFAULT_FROM_EMAIL', default='Warpp <admin@warpp.xyz>'),
        'description': 'This Developer API is part od the BitWarp project developed by @jvacx',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://warpp.xyz/terms/',
        'title': 'Warpp - Developer API',
    },
    'api_version': '1.0',
    'doc_expansion': 'none',
}


# SERVER SETTINGS
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'contrib.renderers.SafeJSONRenderer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'oauth.authentication.SocialAuthentication',
    ],

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.FileUploadParser',
    ),

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ),

    'DEFAULT_PAGINATION_CLASS': 'contrib.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 100,

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


CACHES = {
    'default': env.cache('CACHE_URL', default='locmemcache://warpp.cache')
}


TEST_RUNNER = 'contrib.runner.WarpTestRunner'

# OAUTH 2
OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth.WarpApplication'

# ADMIN TOOLS
ADMIN_TOOLS_MENU = 'contrib.admin.menu.WarpMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'contrib.admin.dashboard.WarpIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'contrib.admin.dashboard.WarpAppIndexDashboard'

# DOCS
API_DOCS_URL = "/docs/"
CORS_ORIGIN_ALLOW_ALL = True


# WARP CONFIGURATION
WEBSITE_NAME = env('WEBSITE_NAME', default='BitWarp')
WEBSITE_AUTHOR = env('WEBSITE_AUTHOR', default='@getwarpp')

TOKEN_EXPIRATION_DAYS = env.int('TOKEN_EXPIRATION_DAYS', default=7)
USE_HTTPS = env.bool('USE_HTTPS', default=False)
DELETE_ACCOUNT_AFTER_DISABLE = env.bool('DELETE_ACCOUNT_AFTER_DISABLE', default=False)
MANAGE_TRANSACTIONS = env.bool('MANAGE_TRANSACTIONS', default=True)
FRONTEND_URL = env('FRONTEND_URL', default='http://client.warpp.xyz/')
BACKEND_URL = env('BACKEND_URL', default='http://warpp.xyz/')

ACTION_ACCOUNT_ACTIVATION = env('ACTION_ACCOUNT_ACTIVATION', default='#/auth/account-activation/')
ACTION_RESET_PASSWORD = env('ACTION_RESET_PASSWORD', default='#/auth/reset-password/')
ACTION_CHANGE_EMAIL = env('ACTION_CHANGE_EMAIL', default='#/auth/change-email/')
ACTION_CANCEL_ACCOUNT = env('ACTION_CANCEL_ACCOUNT', default='#/auth/cancel-account/')


# Blog
WAGTAIL_SITE_NAME = 'jvacx blog'
PUPUT_ENTRY_MODEL = 'blog.models.BlogEntry'
BLOG_ADMIN_EMAIL = 'jvacx.log@gmail.com'

# Analytics
GA_KEY_FILEPATH = join(dirname(PROJECT_DIR), 'service.json')
GA_VIEW_ID = 'ga:126135708'