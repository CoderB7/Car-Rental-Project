"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import core.utils
import environ

from pathlib import Path
from celery.schedules import crontab
from django.urls import reverse_lazy

from core.unfold_conf import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# READING ENV
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret! 
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.str("DEBUG")

ALLOWED_HOSTS = ["*"]

# Application definition

DJANGO_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
]

CUSTOM_APPS = [
    "apps.users",
    "apps.shared",
    "apps.payment",
    "apps.cars",
    "apps.rent",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rosetta",
    'corsheaders',
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "core.authentication.CustomJWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "EXCEPTION_HANDLER": 'core.exception_handler.custom_exception_handler',
    "PAGE_SIZE": 10,
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Car Rental API',
    'DESCRIPTION': 'Car Rental Group',
    'VERSION': 'v1',
    'TERMS_OF_SERVICE': 'https://www.google.com/policies/terms/',
    'CONTACT': {'email': 'info@carrental.group'},
    'LICENSE': {'name': 'BSD License'},
    'SERVE_PUBLIC': True,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'GENERATOR_CLASS': 'core.schema.BothHttpAndHttpsSchemaGenerator',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'PREPROCESSING_HOOKS': [
        'core.hooks.remove_apis_from_list',
    ],
    'SECURITY': [{'BearerAuth': []}, {'CustomJWT': []}],
    'SECURITY_DEFINITIONS': {
        'BearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        },
    },
    # OTHER SETTINGS
    "EXCLUDE_PATH": [reverse_lazy("schema")],
    "SCHEMA_PATH_PREFIX": r"/api/"
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "HOST": env.str("DB_HOST"),
        "PORT": env.str("DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = (BASE_DIR / "staticfiles",)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

###

# CACHES
CACHES = {
    'default': {
        "BACKEND": 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',  # Use the appropriate Redis server URL
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# This is to ensure Django sessions are stored in Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Custom User model
AUTH_USER_MODEL = "users.User"

CORS_ORIGIN_ALLOW_ALL = True # ?
CORS_ALLOW_CREDENTIALS = True # ?

# Email
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.str("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Celery
CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_RESULT_BACKEND = 'redis://redis:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULE = {
    'expire-old-bookings': {
        'task': 'apps.rent.tasks.expire_old_bookings',
        'schedule': crontab(hour='*/1'),  # Run every hour
    },
}


# CONSTANTS
ENCRYPTION_KEY=env.str('ENCRYPTION_KEY').encode()

JWT_ALGORITHM = env.str('JWT_ALGORITHM')
JWT_ACCESS_TOKEN_SECRET=env.str('JWT_ACCESS_TOKEN_SECRET')
JWT_REFRESH_TOKEN_SECRET=env.str('JWT_REFRESH_TOKEN_SECRET')

REFRESH_TOKEN_EXPIRATION_DAYS=env.str('REFRESH_TOKEN_EXPIRATION_DAYS')
ACCESS_TOKEN_EXPIRATION_MINUTES=env.str('ACCESS_TOKEN_EXPIRATION_MINUTES')
JWT_REFRESH_TOKEN_EXPIRATION = env.int('REFRESH_TOKEN_EXPIRATION_DAYS') * 24 * 60 * 60  # in seconds

OTP_LIFETIME = env.str("OTP_LIFETIME")

REDIS_HOST=env.str("REDIS_HOST")
REDIS_PORT=env.str("REDIS_PORT")
REDIS_DB=env.str("REDIS_DB")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
]