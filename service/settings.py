from os import path, environ, makedirs
from pathlib import Path

import pytz
from dotenv import load_dotenv
import logging.config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'

# Create logs directory
makedirs(LOGS_DIR, exist_ok=True)

# Load env file
env_file = environ.get('.env.local', '.env.prod')
load_dotenv(BASE_DIR / env_file)

# Django Settings
DEBUG = (environ.get('DJANGO_DEBUG') == "True")
DEBUG_LEVEL = environ.get('DJANGO_DEBUG_LEVEL')
ALLOWED_HOSTS = environ['DJANGO_ALLOWED_HOSTS'].split(',')

# Azure Settings
SECRET_KEY = environ['DJANGO_SECRET_KEY']
AZURE_TENANT_ID = environ['AZURE_TENANT_ID']
AZURE_CLIENT_ID = environ['AZURE_CLIENT_ID']
AZURE_CLIENT_SECRET = environ['AZURE_CLIENT_SECRET']
ZOHO_SECRET_KEY = environ['ZOHO_SECRET_KEY']
ZOHO_CLIENT_ID = environ['ZOHO_CLIENT_ID']

# Security Settings
SESSION_COOKIE_SECURE = (environ.get('DJANGO_SESSION_COOKIE_SECURE') == "True")
CSRF_COOKIE_SECURE = (environ.get('DJANGO_CSRF_COOKIE_SECURE') == "True")
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'

# Celery Settings
CELERY_BROKER_URL = f'redis://{environ["REDIS_HOST"]}:{environ["REDIS_PORT"]}/0'
CELERY_RESULT_BACKEND = f'redis://{environ["REDIS_HOST"]}:{environ["REDIS_PORT"]}/1'

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://99.244.215.155:3000',
        'https://unify.experiorheadoffice.ca'
    ]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework',
    "rest_framework_api_key",
    'corsheaders',
    'celery',
    'service',
    'core',
    'api',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.auth.authentication.AzureADAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{environ["REDIS_HOST"]}:{environ["REDIS_PORT"]}',
    }
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.APIKeyDetectionMiddleware',
    'core.middleware.AuditMiddleware',
]

LOGGING_CONFIG = None
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s [%(levelname)s] [%(name)s]: %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': path.join(LOGS_DIR, 'django-service.log'),
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': DEBUG_LEVEL,
            'propagate': True,
        },
        "gunicorn.error": {
            "handlers": ["file", "console"],
            "level": DEBUG_LEVEL,
            "propagate": False,
        },
        "gunicorn.access": {
            "handlers": ["file", "console"],
            "level": DEBUG_LEVEL,
            "propagate": False,
        },
        'core': {
            'handlers': ['file', 'console'],
            'level': DEBUG_LEVEL,
            'propagate': False,
        },
        'api': {
            'handlers': ['file', 'console'],
            'level': DEBUG_LEVEL,
            'propagate': False,
        },
    },
})

ROOT_URLCONF = 'service.urls'

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = path.join(BASE_DIR, "media")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR, 'templates')
        ],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': environ['DATABASE_NAME'],
        'USER': environ['DATABASE_USERNAME'],
        'PASSWORD': environ['DATABASE_PASSWORD'],
        'HOST': environ['DATABASE_HOST'],
        'PORT': environ['DATABASE_PORT'],
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'service.wsgi.application'