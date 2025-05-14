import os
import dj_database_url

from pathlib import Path
from dotenv import load_dotenv


# importing external congigs for additional settings values
from .addons.asgi_config import *
from .addons.installed_apps import *
from .addons.middlware import *


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


SECRET_KEY = "django-insecure-vq$2fk&_667c9w#g)=$ew5ge$l2@8l^^x7ne)uu5*j)@+rsr6("

# DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

DEBUG = True
ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "projectile_settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
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

WSGI_APPLICATION = "settings.settings.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "chat_app_db",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


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

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # required for /auth/login
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "...",
    "DESCRIPTION": "---",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
}


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.User"

PHONENUMBER_DEFAULT_REGION = "BD"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
