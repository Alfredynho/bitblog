# -*- encoding:utf-8 -*-

from __future__ import absolute_import, unicode_literals
import environ
import sys
from os.path import join, dirname

PROJECT_PATH = dirname(dirname(dirname(__file__)))
APPS_PATH = join(PROJECT_PATH, "apps")
env = environ.Env()
env.read_env(join(PROJECT_PATH, ".environment"))

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    # 'django.contrib.humanize',

    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (

    # Blog
    'wagtail.contrib.wagtailsitemaps',
    'wagtail.contrib.wagtailroutablepage',
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',
    'wagtail.wagtailadmin',
    'wagtail.wagtailcore',

    # Blog utils
    'wagalytics',
    'wagtailfontawesome',
    'wagtail.contrib.settings',
    'wagtail.contrib.wagtailstyleguide',
    "wagtail.contrib.table_block",


    # Templating
    'overextends',
    'compressor',
    'import_export',

    'modelcluster',
    'taggit',

    # Accounts
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',

    # Authentication
    'oauth2_provider',

    # API Rest
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',

    # Settings
    'constance',
)

LOCAL_APPS = (
    # custom users app
    'apps.users.app.UsersConfig',
    'apps.credentials',
    'apps.contrib',
    'apps.blog',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # Wagtail middlewares
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)
# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'apps.contrib.sites.migrations'
}
# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', False)
# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
FIXTURE_DIRS = (
    join(APPS_PATH, "fixtures"),
)
# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST, EMAIL_PORT = '127.0.0.1', 1025  # Work with MailHog
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Warpp <admin@warpp.xyz>')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
ADMINS = (
    ("Admin", 'admin@warpp.xyz'),
)
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env.db("DATABASE_URL", default="sqlite://%s" % dirname(PROJECT_PATH) + '/development.db'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

if 'test' in sys.argv:
    DATABASES = {
        'default': env.db("TEST_DATABASE_URL", default="sqlite://%s" % dirname(PROJECT_PATH) + '/testing.db'),
    }
    # DATABASES['default']['NAME'] = "test_%s" % DATABASES['default']['NAME']


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'es-BO'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True


# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(APPS_PATH, 'templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
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
                'apps.contrib.context_processors.website',
            ],

        },
    },
]
# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
STATIC_ROOT = join(PROJECT_PATH, 'public/static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    join(APPS_PATH, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
MEDIA_ROOT = join(PROJECT_PATH, 'public/media')
MEDIA_URL = '/media/'
# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ADMIN_URL = r'^admin/'
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# Some really nice defaults


AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:view-dashboard'
LOGIN_URL = 'account_login'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['warpp.xyz'])

# INSTALLED_APPS += ('kombu.transport.django',)
# BROKER_URL = env('CELERY_BROKER_URL', default='django://')
# if BROKER_URL == 'django://':
#     CELERY_RESULT_BACKEND = 'redis://'
# else:
#     CELERY_RESULT_BACKEND = BROKER_URL

# CACHE CONFIGURATION
# ------------------------------------------------------------------------------
# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#     }
# }

# django-compressor
# ------------------------------------------------------------------------------
# INSTALLED_APPS += ("compressor", )
# STATICFILES_FINDERS += ("compressor.finders.CompressorFinder", )


# REST FRAMEWORK CONFIGURATION
# ------------------------------------------------------------------------------
# OAUTH 2
OAUTH2_PROVIDER_APPLICATION_MODEL = 'credentials.PlatformApp'
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {

    'EXCEPTION_HANDLER': 'apps.contrib.api.exceptions.formatted_exception_handler',
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_RENDERER_CLASSES': (
        'apps.contrib.renderers.SafeJSONRenderer',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ],

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ),

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.TemplateHTMLRenderer'
    ),

    'DEFAULT_PAGINATION_CLASS': 'apps.contrib.api.pagination.LinkHeaderPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.AcceptHeaderVersioning',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


# PLATFORM SETTINGS
# ------------------------------------------------------------------------------
PROJECT_NAME = "Warpp"
PROJECT_AUTHOR = "Warpp Team"
PROJECT_DOMAIN = "http://warpp.xyz"
TOKEN_EXPIRATION_DAYS = env.int('TOKEN_EXPIRATION_DAYS', default=7)
MANAGE_TRANSACTIONS = env.bool('MANAGE_TRANSACTIONS', default=True)
CONSTANCE_CONFIG = {
    'LAUNCH_DATE': (42, 'Answer to the Ultimate Question of Life, The Universe, and Everything'),
}
# ADMIN TOOLS
ADMIN_TOOLS_MENU = 'apps.contrib.admin.menu.Menu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'apps.contrib.admin.dashboard.IndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'apps.contrib.admin.dashboard.AppIndexDashboard'

# Settings to OLD swagger # TODO Update this
API_DOCS_URL = "docs"
PLATFORM_DOCS_URL = "https://docs.chuspita.net"
SWAGGER_SETTINGS = {
    'info': {
        'contact': env('DEFAULT_FROM_EMAIL', default='Warpp <admin@warpp.xyz>'),
        'description': 'Developer API for Warpp project',
        'license': 'Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'http://warpp.xyz/terms/',
        'title': 'Developer API',
    },
    'api_version': '1.0',
    'doc_expansion': 'none',
}


# ALLAUTH CONFIGURATION
# ------------------------------------------------------------------------------
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'apps.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'apps.users.adapters.SocialAccountAdapter'
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_USERNAME_BLACKLIST = ["vicobits", "admin"]
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'https'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.8'
    },
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}


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
            'filename': '%s/django.log' % join(PROJECT_PATH, 'var/log'),
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

# Blog
WAGTAIL_SITE_NAME = 'VicoBits blog'
PUPUT_ENTRY_MODEL = 'blog.models.BlogEntry'
BLOG_ADMIN_EMAIL = 'victoraguilar.net@gmail.com'

# Analytics
GA_KEY_FILEPATH = join(PROJECT_PATH, 'service.json')
GA_VIEW_ID = 'ga:126135708'
