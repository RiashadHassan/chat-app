import os

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
PROJECT_APPS = [
    "aquila",
    "base",
    "core",
    "connection",
    "chat",
    "server",
    "member",
    "message",
    "permission",
    "health",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_extensions",
    "phonenumber_field",
    "drf_spectacular",
    "silk",
    "django_elasticsearch_dsl",
    "corsheaders",
    "storages",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

if os.environ.get("DAPHNE", "FALSE").lower() in ("true", "1", "yes"):
    INSTALLED_APPS = ["daphne"] + INSTALLED_APPS
