import os

from pathlib import Path
from dotenv import load_dotenv


# importing external congigs for additional settings values
from .config import *

# BASE_DIR is chat-app/projectile where manage.py is located
BASE_DIR = Path(__file__).resolve().parent.parent

# .env is inside chat-app/projectile
# this is a bit messy, but works for now
# TODO: restructure project to have .env at chat-app level
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

CORS_ALLOW_ALL_ORIGINS = True

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

if DEBUG:
    MIDDLEWARE = MIDDLEWARE + SILK_MIDDLEWARE

ALLOWED_HOSTS = ["*"]

ROOT_URLCONF = "projectile_settings.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.parent / "templates",
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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.User"

PHONENUMBER_DEFAULT_REGION = "BD"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STORAGES = {
    # media file management (images in s3)
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")


AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
