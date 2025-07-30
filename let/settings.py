# let/settings.py

import os
from pathlib import Path
from decouple import config # Import the config function
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE DJANGO SETTINGS (READ FROM .ENV) ---
# The secret key is now read from the .env file.
SECRET_KEY = config('SECRET_KEY')

# The DEBUG setting is now a boolean read from the .env file.
# The `cast=bool` is important to convert the string 'True' to a boolean True.
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS is now a comma-separated list in the .env file.
# The `config` function with `cast=lambda v: [s.strip() for s in v.split(',')]`
# correctly parses it into a Python list.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_celery_results",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt",
    "myapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "let.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "let.wsgi.application"

# --- DATABASE (READ FROM .ENV) ---
DATABASES = {
    "default": {
        "ENGINE": config('DB_ENGINE'),
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER'),
        "PASSWORD": config('DB_PASSWORD'),
        "HOST": config('DB_HOST'),
        "PORT": config('DB_PORT', cast=int),
    }
}

# --- PASSWORD VALIDATION (NO CHANGE) ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- INTERNATIONALIZATION (NO CHANGE) ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- OLD TEMPLATE-BASED AUTH SETTINGS (CAN BE REMOVED LATER) ---
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "login"

# --- CELERY (READ FROM .ENV) ---
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True

# --- CORS (READ FROM .ENV) ---
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOW_CREDENTIALS = True

# --- DJANGO REST FRAMEWORK SETTINGS ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
}

# --- SIMPLE JWT SETTINGS ---
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}
# TEMPORARY DEBUGGING LINES - REMOVE AFTER FIXING
