"""
Django settings for nameless_project project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

from pathlib import Path

from django.utils.translation import gettext_lazy as _

from . import env

PROJECT_VERSION = "0.1.0"

# This is the nameless_project directory
BASE_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

SERVER_NAME = env.str("SERVER_NAME")
SERVER_PROTOCOL = env.str("SERVER_PROTOCOL", "https")
SERVER_PREFIX = f"{SERVER_PROTOCOL}://{SERVER_NAME}"
SITE_NAME = env.str("SITE_NAME", SERVER_NAME)
SITE_ID = 1
if SERVER_PROTOCOL == "https":
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_HOST = SERVER_NAME
    SECURE_SSL_REDIRECT = True

ANALYTICS_GTAG = env.get("ANALYTICS_GTAG")

DEBUG = env.bool("DJANGO_DEBUG", False)
DEBUG_SQL = env.bool("DJANGO_DEBUG_SQL", False)
DEBUG_SQL_LIMIT = env.int("DJANGO_DEBUG_SQL_LIMIT", 5)
DEBUG_TOOLBAR = env.bool("DJANGO_DEBUG_TOOLBAR", False)
LOGGING_PATH = env.get("LOGGING_PATH")
LOGGING_LEVEL = env.str("LOGGING_LEVEL", "INFO")

X_FRAME_OPTIONS = "DENY"
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS") or [SERVER_NAME]
ADMINS = [(email, email) for email in env.list("DJANGO_ADMINS")]

EMAIL_HOST = env.get("DJANGO_EMAIL_HOST")
EMAIL_HOST_USER = env.get("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.get("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT", 0)
EMAIL_USE_TLS = env.bool("DJANGO_EMAIL_USE_TLS", None)
EMAIL_USE_SSL = env.bool("DJANGO_EMAIL_USE_SSL", None)
EMAIL_BACKEND = env.str("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_FILE_PATH = env.get("DJANGO_EMAIL_FILE_PATH")

DEFAULT_FROM_EMAIL = env.get("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = env.str("SERVER_EMAIL", "root@localhost")

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_rq",
    "django_extensions",
    "django_uwsgi",
    "nameless_project.apps.CustomAdminConfig",
    "nameless.apps.NamelessConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = env.str("DJANGO_ROOT_URLCONF", "nameless_project.urls")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django_settings_export.settings_export",
            ],
        },
    }
]

SETTINGS_EXPORT = [
    "ANALYTICS_GTAG",
    "DEBUG",
    "PROJECT_VERSION",
    "SERVER_NAME",
    "SERVER_PREFIX",
    "SERVER_PROTOCOL",
    "SITE_NAME",
]

WSGI_APPLICATION = "nameless_project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": True,
        "ENGINE": "django.db.backends.postgresql",
        "HOST": env.get("DJANGO_DB_HOST"),
        "NAME": env.get("DJANGO_DB_NAME"),
        "PASSWORD": env.get("DJANGO_DB_PASSWORD"),
        "USER": env.get("DJANGO_DB_USER"),
    }
}

CACHES = {
    "default": {
        "BACKEND": env.str(
            "DJANGO_CACHE_BACKEND",
            "django.core.cache.backends.dummy.DummyCache" if DEBUG else "django.core.cache.backends.locmem.LocMemCache",
        ),
        "KEY_PREFIX": env.get("DJANGO_CACHE_KEY_PREFIX"),
        "LOCATION": env.get("DJANGO_CACHE_LOCATION"),
        "TIMEOUT": env.int("DJANGO_CACHE_TIMEOUT", 0) or None,
    }
}

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en", _("English")),
]

LOCALE_PATHS = [
    "/app/src/locale",
]

TIME_ZONE = "Europe/Bucharest"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/var/app/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_ROOT = "/var/app/media/"

MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT", 6379)
REDIS_DB = env.int("REDIS_DB", 0)
REDIS_PASSWORD = env.get("REDIS_PASSWORD")
REDIS_SOCKET_TIMEOUT = env.int("REDIS_SOCKET_TIMEOUT", 10)

RQ_QUEUES = {
    "default": {
        "HOST": REDIS_HOST,
        "PORT": REDIS_PORT,
        "DB": REDIS_DB,
        "PASSWORD": REDIS_PASSWORD,
        "SOCKET_TIMEOUT": REDIS_SOCKET_TIMEOUT,
        "DEFAULT_TIMEOUT": 24 * 60 * 60,  # 24h - allow long-running tasks
    },
}
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s.%(msecs)d] %(name)s (%(levelname)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "WARNING",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "root": {
        "level": LOGGING_LEVEL,
        "handlers": ["console", "mail_admins"],
    },
    "loggers": {
        "django.request": {"level": LOGGING_LEVEL},
        "django.db.backends": {"level": LOGGING_LEVEL},
        "uvicorn": {"propagate": True},
        "asyncio": {"level": "INFO"},
        "parso": {"level": "WARNING"},
        "httpcore": {"level": "WARNING"},
        "httpx": {"level": "WARNING"},
    },
    "filters": {},
}


# Advanced debug settings
SENTRY_DSN = env.get("SENTRY_DSN")
if SENTRY_DSN:
    import logging

    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    from sentry_sdk.integrations.logging import ignore_logger

    ignore_logger("django.security.DisallowedHost")
    sentry_sdk.init(
        release=f"nameless_project@{PROJECT_VERSION}",
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        send_default_pii=True,
        auto_session_tracking=False,
    )

if DEBUG_SQL:
    import sys
    from traceback import format_stack

    from sqlparse import format as sqlformat

    class SQLFormatFilter:
        def __init__(self, skip=(), limit=5):
            self.skip = [__name__, "logging"]
            self.skip.extend(skip)
            self.limit = limit

        def filter(self, record):
            if not getattr(record, "__sql_format_patched__", False):
                frame = sys._getframe(1)
                if self.limit:
                    while any(skip for skip in self.skip if frame.f_globals.get("__name__", "").startswith(skip)):
                        frame = frame.f_back
                    stack = "".join(f"\33[1;30m{line}\33[0m" for line in format_stack(f=frame, limit=self.limit))
                    stack = f"\n \33[1;32m-- stack: \n{stack}\33[0m"
                else:
                    stack = ""
                if hasattr(record, "duration") and hasattr(record, "sql") and hasattr(record, "params"):
                    sql = "\n  ".join(f"\33[33m{line}\33[0m" for line in sqlformat(record.sql or "", reindent=True).strip().splitlines())
                    record.msg = (
                        f"\33[31mduration: \33[{'' if record.duration < 0.1 else '1;'}31m{record.duration:.4f} secs\33[0m, "
                        f"\33[33marguments: \33[1{';33' if record.params else ''}m{record.params}\33[0m"
                        f"\n  {sql}{stack}"
                    )
                    record.args = ()
                elif stack:
                    record.msg += stack

                record.__sql_format_patched__ = True
            return True

    LOGGING["loggers"]["django.db.backends"]["level"] = "DEBUG"
    LOGGING["loggers"]["django.db.backends"]["filters"] = ["sql_format"]
    LOGGING["filters"]["sql_format"] = {
        "()": SQLFormatFilter,
        "skip": ("django.db", "__main__"),
        "limit": DEBUG_SQL_LIMIT,
    }

if LOGGING_PATH:
    LOGGING["handlers"]["logfile"] = {
        "level": "INFO",
        "class": "logging.handlers.WatchedFileHandler",
        "encoding": "utf-8",
        "filename": f"{LOGGING_PATH}/application.log",
        "formatter": "verbose",
    }
    LOGGING["handlers"]["debugfile"] = {
        "level": "DEBUG",
        "class": "logging.handlers.WatchedFileHandler",
        "encoding": "utf-8",
        "filename": f"{LOGGING_PATH}/debug.log",
        "formatter": "verbose",
    }
    LOGGING["root"]["handlers"] = ["logfile", "debugfile"]
    LOGGING["loggers"]["django.request"]["handlers"] = ["logfile"]
    LOGGING["loggers"]["django.db.backends"]["handlers"] = ["debugfile"]

if DEBUG:
    INSTALLED_APPS += [
        "rosetta",
    ]

if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda _: DEBUG,
    }
    DEBUG_TOOLBAR_PANELS = [
        "django_uwsgi.panels.UwsgiWorkersPanel",
        "django_uwsgi.panels.UwsgiActionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]
