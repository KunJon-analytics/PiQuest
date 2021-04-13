from pathlib import Path
import os

import environ

env = environ.Env(
    DEBUG=(bool, False)
)

READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    environ.Env.read_env()

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Created Apps
    'user',
    'main',
    'projects',
    'contact',

    # Django Apps
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-Party Apps
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
]

SITE_ID=1

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
STATIC_ROOT = "static_root"
MEDIA_URL = '/media/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

TAILWIND_APP_NAME = 'theme'

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

AUTH_USER_MODEL = 'user.User'

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
SERVER_EMAIL = 'contact@piquest.com'
DEFAULT_FROM_EMAIL = 'no-reply@piquest.com'
EMAIL_SUBJECT_PREFIX = '[PiQuest] '
MANAGERS = (
    ('Us', 'ourselves@piquest.com'),
)

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = 'tailwind'

from django.urls import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('quiz:quiz_index')
LOGIN_URL = reverse_lazy('account_login')
LOGOUT_URL = reverse_lazy('account_logout')

INTERNAL_IPS = [
    # ...
    '127.0.0.1',
    # ...
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_USERNAME_BLACKLIST = ['activate','create','disable','login','logout','password','profile',]
