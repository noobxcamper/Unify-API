from os import path, environ
from pathlib import Path
from dotenv import load_dotenv

# Load env file
load_dotenv('.env.local')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ['DJANGO_SECRET_KEY']
AZURE_TENANT_ID = environ['AZURE_TENANT_ID']
AZURE_CLIENT_ID = environ['AZURE_CLIENT_ID']
AZURE_CLIENT_SECRET = environ['AZURE_CLIENT_SECRET']
ZOHO_SECRET_KEY = environ['ZOHO_SECRET_KEY']
ZOHO_CLIENT_ID = environ['ZOHO_CLIENT_ID']

DEBUG = (environ.get('DJANGO_DEBUG') == "True")

### Security Settings ###
SESSION_COOKIE_SECURE = (environ.get('DJANGO_SESSION_COOKIE_SECURE') == "True")
CSRF_COOKIE_SECURE = (environ.get('DJANGO_CSRF_COOKIE_SECURE') == "True")
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Lax'

ALLOWED_HOSTS = [
    environ['DJANGO_ALLOWED_HOSTS']
]

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
else:
    CORS_ALLOWED_ORIGINS = [
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
    'service',
    'corsheaders',
    'core',
    'api'
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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

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
        'ENGINE': 'django.db.backends.postgresql',
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

# Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'c:\\users\\hazem\\Desktop\\django-service.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

WSGI_APPLICATION = 'service.wsgi.application'