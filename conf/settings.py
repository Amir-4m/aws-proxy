"""
Django settings for dns_ip_domain project.

Generated by 'django-admin startproject' using Django 1.11.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import ast
import os
from datetime import timedelta

from decouple import config, Csv
from pathlib import Path

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)
DEVEL = config("DEVEL", default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# Application definition
INSTALLED_APPS = [
    'jsoneditor',
    # 'import_export',
    # 'django_celery_beat',
    'rest_framework',

    'apps.servers',
    'apps.dns',
    'apps.proxies',
    'apps.inspectors',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASS'),
        'HOST': config('DB_HOST', default=""),
        'PORT': config('DB_PORT', default=""),
        # 'OPTIONS': {'charset': 'utf8mb4'}
    }
}

CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': config('CACHE_HOST', default=''),
        'KEY_PREFIX': 'AWS'  # Todo change key_prefix
    },
}

CELERY_BROKER_URL = 'amqp://%(USER)s:%(PASS)s@%(HOST)s' % {
    'USER': config('CELERY_USER'),
    'PASS': config('CELERY_PASS'),
    'HOST': config('CELERY_HOST'),
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/
USE_TZ = True
TIME_ZONE = 'Asia/Tehran'

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOGGING = ({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(LOG_DIR, 'django.log'),
        },
    },
    'loggers': {
        'apps.servers': {
            'level': 'DEBUG',
            'handlers': ['file', 'console']
        },
        'apps.dns': {
            'level': 'DEBUG',
            'handlers': ['file', 'console']
        },
    }
})

# IMPORT_EXPORT_USE_TRANSACTIONS = True
# IMPORT_EXPORT_SKIP_ADMIN_LOG = True
JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.css'

CLOUDFLARE_EMAIL = config('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_KEY = config('CLOUDFLARE_API_KEY')

SERVER_EXPIRY_TIME = config('SERVER_EXPIRY_MINUTE', default=60)
UPDATED_SERVER_PERCENTAGE = config('UPDATED_SERVER_PERCENTAGE', default=10, cast=int)

MAX_RANDOM_CODE = config('MAX_RANDOM_CODE', default=5, cast=int)
CLEAR_INSPECTOR_LOGS_CRONTAB = ast.literal_eval(config("CLEAR_INSPECTOR_LOGS_CRONTAB"))
CLEAR_DNS_LOGS_CRONTAB = ast.literal_eval(config("CLEAR_DNS_LOGS_CRONTAB"))
CLEAR_SERVER_LOGS_CRONTAB = ast.literal_eval(config("CLEAR_SERVER_LOGS_CRONTAB"))
AWS_PROXY = config('AWS_PROXY', default='')
