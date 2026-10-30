import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "local-only-not-used-for-end-user-auth")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
ALLOWED_HOSTS = [x for x in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if x]

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "corsheaders", "rest_framework", "django_filters",
    "accounts", "fleet", "warehouse", "shipments", "scheduling", "dashboard", "notifications",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware", "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND": "django.template.backends.django.DjangoTemplates", "DIRS": [], "APP_DIRS": True,
              "OPTIONS": {"context_processors": ["django.template.context_processors.request", "django.contrib.auth.context_processors.auth", "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("Set DATABASE_URL, for example mysql://logicraft:password@127.0.0.1:3306/logicraft")
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=60)}
if DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
    DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4", "init_command": "SET sql_mode='STRICT_TRANS_TABLES'"}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS = [x for x in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",") if x]
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_JWT_AUDIENCE = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated")
ENABLE_LOCAL_AUTH = os.getenv("ENABLE_LOCAL_AUTH", str(not bool(SUPABASE_URL))).lower() == "true"
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["accounts.authentication.SupabaseJWTAuthentication", "accounts.authentication.LocalSessionAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend", "rest_framework.filters.SearchFilter", "rest_framework.filters.OrderingFilter"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "config.exceptions.api_exception_handler",
}

