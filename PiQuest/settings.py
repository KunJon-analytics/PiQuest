from django.urls import reverse_lazy
from pathlib import Path
import os

import environ

from django.contrib.messages import constants as messages

env = environ.Env(
    DEBUG=(bool, False)
)

READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    environ.Env.read_env()

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
CMC_PRO_API_KEY = env('CMC_PRO_API_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    # Created Apps
    'user',
    'main',
    'projects',
    'contact',
    'wagtail.core',
    'wagtail.admin',
    'wagtail.documents',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.search',
    'wagtail.sites',
    'wagtail.contrib.redirects',
    'wagtail.contrib.forms',
    'wagtail.contrib.sitemaps',
    'wagtail.contrib.routable_page',
    'taggit',
    'modelcluster',
    'django_social_share',
    'puput',
    'colorful',
    'classroom',
    'digiwiz',
    'ckeditor',
    'ckeditor_uploader',
    'classroom.templatetags.custom_tags',
    'sorl.thumbnail',
    'star_ratings',

    # Django Apps
    'whitenoise.runserver_nostatic',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-Party Apps
    'allauth_bootstrap4',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'quiz',
    'multichoice',
    'true_false',
    'essay',
    'crispy_forms',
    'crispy_tailwind',
    'tailwind',
    'theme',
    'debug_toolbar',
    'guardian',
    'mathfilters',
    'pinax.badges',
    'pinax.announcements',
    'imagekit',
    'pinax.events',
    'storages',
    'todo',
    'webpack_loader',
]

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width': 1110,
        'toolbar_Custom': [
            ['Font', 'FontSize', 'TextColor', 'BGColor'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript'],
            ['Undo', 'Redo', 'JustifyLeft', 'JustifyCenter',
                'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Image', 'Table', 'HorizontalRule', 'NumberedList',
             'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote',
             'BidiLtr', 'BidiRtl'],
            ['RemoveFormat', 'Smiley', 'SpecialChar'],
            ['Styles', 'Format'],
            ['Youtube'],
            ['Source']
        ],
        'extraPlugins': 'youtube',
    },
}

SITE_ID = 1

WAGTAIL_SITE_NAME = 'PiQuests'

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE_CLASSES = (
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
)

ROOT_URLCONF = 'PiQuest.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'PiQuest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)


TAILWIND_APP_NAME = 'theme'

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

AUTH_USER_MODEL = 'user.User'

TEMPLATE_CONTEXT_PROCESSOR = 'django.core.context_processors.request'
STAR_RATINGS_STAR_HEIGHT = 20

CKEDITOR_UPLOAD_PATH = 'uploads/lessons/'


# MESSAGE_TAGS = {
#     messages.DEBUG: 'alert-secondary',
#     messages.INFO: 'alert-info',
#     messages.SUCCESS: 'alert-success',
#     messages.WARNING: 'alert-warning',
#     messages.ERROR: 'alert-danger',
# }

# Logging
# https://docs.djangoproject.com/en/1.8/topics/logging/

# from .log_filters import ManagementFilter

# verbose = (
#     "[%(asctime)s] %(levelname)s "
#     "[%(name)s:%(lineno)s] %(message)s")

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'remove_migration_sql': {
#             '()': ManagementFilter,
#         },
#     },
#     'handlers': {
#         'console': {
#             'filters': ['remove_migration_sql'],
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'formatters': {
#         'verbose': {
#             'format': verbose,
#             'datefmt': "%Y-%b-%d %H:%M:%S"
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'formatter': 'verbose'
#         },
#     },
# }


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'contact@mg.piquests.com'
DEFAULT_FROM_EMAIL = 'no-reply@mg.piquests.com'
EMAIL_SUBJECT_PREFIX = '[PiQuests] '
MANAGERS = (
    ('Us', 'piquests@gmail.com'),
)

# CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap4', 'tailwind')

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# CRISPY_TEMPLATE_PACK = 'tailwind'


LOGIN_REDIRECT_URL = reverse_lazy('quiz:quiz_index')
LOGIN_URL = reverse_lazy('account_login')
LOGOUT_URL = reverse_lazy('account_logout')

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

PI_VALIDATION_KEY = env('PI_VALIDATION_KEY')

PIQUESTS_PK = env('PIQUESTS_PK')

TELEGRAM = {
    'bot_token': env('PIQUESTS_BOT'),
    'channel_name': 'PiQuestsAnnouncements',
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_USERNAME_BLACKLIST = ['activate', 'create',
                              'disable', 'login', 'logout', 'password', 'profile', ]


if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"

    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.piquests.com']
    SITE_ID = 2

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = True
    EMAIL_PORT = env("EMAIL_PORT")
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")

    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_FILE_OVERWRITE = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_REGION_NAME = 'FRA1'
    AWS_S3_ENDPOINT_URL = 'https://fra1.digitaloceanspaces.com'

    CMC_PRO_API_KEY = env('CMC_PRO_API_KEY')
    PI_VALIDATION_KEY = env('PI_VALIDATION_KEY')
    PIQUESTS_PK = env('PIQUESTS_PK')

    COMPRESS_OFFLINE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

PUPUT_AS_PLUGIN = True

TODO_STAFF_ONLY = False

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)
