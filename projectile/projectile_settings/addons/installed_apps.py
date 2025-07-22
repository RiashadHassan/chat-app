ON_TOP_APPS = [
    "daphne",
]
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
    "chat",
    "server",
    "member",
    "permission",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_extensions",
    "phonenumber_field",
    "drf_spectacular",
    "silk",
    "django_elasticsearch_dsl",
    "corsheaders",
]

INSTALLED_APPS = ON_TOP_APPS + DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS
