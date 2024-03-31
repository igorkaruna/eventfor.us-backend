import os
from datetime import timedelta
from pathlib import Path

from environs import Env


env = Env()
env.read_env(override=True)


# ENV configurations

with env.prefixed("POSTGRES_"):
    POSTGRES_DATABASE = {
        "ENGINE": env.str("ENGINE"),
        "NAME": env.str("DB"),
        "USER": env.str("USER"),
        "PASSWORD": env.str("PASSWORD"),
        "HOST": env.str("HOST"),
        "PORT": env.str("PORT"),
    }

with env.prefixed("JWT_"):
    JWT_CONFIGURATION = {
        "ACCESS_TOKEN_LIFETIME_DAYS": env.int("ACCESS_TOKEN_LIFETIME_DAYS"),
        "REFRESH_TOKEN_LIFETIME_DAYS": env.int("REFRESH_TOKEN_LIFETIME_DAYS"),
    }

with env.prefixed("SECURE_"):
    SECURITY_CONFIGURATION = {
        "SSL_REDIRECT": env.bool("SSL_REDIRECT"),
        "HSTS_SECONDS": env.int("HSTS_SECONDS"),
        "HSTS_INCLUDE_SUBDOMAINS": env.bool("HSTS_INCLUDE_SUBDOMAINS"),
        "HSTS_PRELOAD": env.bool("HSTS_PRELOAD"),
        "CONTENT_TYPE_NOSNIFF": env.bool("CONTENT_TYPE_NOSNIFF"),
        "SESSION_COOKIE": env.bool("SESSION_COOKIE"),
        "CSRF_COOKIE": env.bool("CSRF_COOKIE"),
        "REFERRER_POLICY": env.str("REFERRER_POLICY"),
    }


with env.prefixed("LOGGER_"):
    LOGGER_CONFIGURATION = {
        "CONSOLE_LEVEL": env.str("CONSOLE_LEVEL"),
        "FILE_LEVEL": env.str("FILE_LEVEL"),
    }

# Django settings

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
INTERNAL_IPS = env.list("INTERNAL_IPS")


INSTALLED_APPS = [
    # default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3-rd party
    "django_filters",
    "debug_toolbar",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    # local
    "events.apps.EventsConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    # default
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 3-rd party
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "request_logging.middleware.LoggingMiddleware",
    # local
    "base.middlewares.ExceptionHandlingMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

AUTH_USER_MODEL = "users.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "en-us"
ROOT_URLCONF = "base.urls"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = "base.wsgi.application"

DATABASES = {
    "default": POSTGRES_DATABASE,
}

# Logger

LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": LOGGER_CONFIGURATION["CONSOLE_LEVEL"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": LOGGER_CONFIGURATION["FILE_LEVEL"],
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "eventfor.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"] if DEBUG else ["file"],
            "level": LOGGER_CONFIGURATION["CONSOLE_LEVEL"] if DEBUG else LOGGER_CONFIGURATION["FILE_LEVEL"],
            "propagate": True,
        },
    },
}

# Rest Framework and DJT settings

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": env.int("PAGE_SIZE"),
}

if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)

# JWT settings

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=JWT_CONFIGURATION["ACCESS_TOKEN_LIFETIME_DAYS"]),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=JWT_CONFIGURATION["REFRESH_TOKEN_LIFETIME_DAYS"]),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Security settings

SECURE_SSL_REDIRECT = SECURITY_CONFIGURATION["SSL_REDIRECT"]
SECURE_HSTS_SECONDS = SECURITY_CONFIGURATION["HSTS_SECONDS"]
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURITY_CONFIGURATION["HSTS_INCLUDE_SUBDOMAINS"]
SECURE_HSTS_PRELOAD = SECURITY_CONFIGURATION["HSTS_PRELOAD"]
SECURE_CONTENT_TYPE_NOSNIFF = SECURITY_CONFIGURATION["CONTENT_TYPE_NOSNIFF"]
SESSION_COOKIE_SECURE = SECURITY_CONFIGURATION["SESSION_COOKIE"]
CSRF_COOKIE_SECURE = SECURITY_CONFIGURATION["CSRF_COOKIE"]
SECURE_REFERRER_POLICY = SECURITY_CONFIGURATION["REFERRER_POLICY"]
