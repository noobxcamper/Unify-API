from os import path, makedirs
from pathlib import Path
import logging.config

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"

# Create logs directory
makedirs(LOGS_DIR, exist_ok=True)

# Environment
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# Django Settings
DEBUG = env.bool("DJANGO_DEBUG", default=False)
DEBUG_LEVEL = env("DJANGO_DEBUG_LEVEL", default="INFO")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])

# Azure / App Settings
SECRET_KEY = env("DJANGO_SECRET_KEY")
AZURE_TENANT_ID = env("AZURE_TENANT_ID", default="")
AZURE_CLIENT_ID = env("AZURE_CLIENT_ID", default="")
AZURE_CLIENT_SECRET = env("AZURE_CLIENT_SECRET", default="")
ZOHO_SECRET_KEY = env("ZOHO_SECRET_KEY", default="")
ZOHO_CLIENT_ID = env("ZOHO_CLIENT_ID", default="")

# Security Settings
SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=not DEBUG)
CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=not DEBUG)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# Celery / Redis Settings
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
    }
}

# CORS
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOWED_ORIGINS = env.list(
        "DJANGO_CORS_ALLOWED_ORIGINS",
        default=[
            "http://localhost:3000",
            "http://99.244.215.155:3000",
            "https://unify.experiorheadoffice.ca",
        ],
    )
    CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django_celery_beat",
    "rest_framework",
    "rest_framework_api_key",
    "corsheaders",
    "celery",
    "service",
    "core",
    "api",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.auth.authentication.AzureADAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.APIKeyDetectionMiddleware",
    "core.middleware.AuditMiddleware",
]

LOGGING_CONFIG = None
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": path.join(LOGS_DIR, "django-service.log"),
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": DEBUG_LEVEL,
            "propagate": True,
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
        "core": {
            "handlers": ["file", "console"],
            "level": DEBUG_LEVEL,
            "propagate": False,
        },
        "api": {
            "handlers": ["file", "console"],
            "level": DEBUG_LEVEL,
            "propagate": False,
        },
    },
})

ROOT_URLCONF = "service.urls"

STATIC_URL = "/static/"
STATIC_ROOT = path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = path.join(BASE_DIR, "media")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USERNAME"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
WSGI_APPLICATION = "service.wsgi.application"