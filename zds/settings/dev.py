import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from colorlog import ColoredFormatter
from django.core.exceptions import ImproperlyConfigured

from . import celery
from .abstract_base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]  # allow everything in case we are in a Docker container

INSTALLED_APPS += (
    "debug_toolbar",
    "django_extensions",
)

MIDDLEWARE = (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "zds.middlewares.nocacheindevmiddleware.NoCacheInDevMiddleware",
) + MIDDLEWARE

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": ColoredFormatter,
            "format": "%(log_color)s %(levelname)s %(reset)s %(bold_black)s%(name)s%(reset)s %(message)s",
            "log_colors": {
                "DEBUG": "fg_white,bg_black",
                "INFO": "fg_black,bg_bold_white",
                "WARNING": "fg_black,bg_bold_yellow",
                "ERROR": "fg_bold_white,bg_bold_red",
                "CRITICAL": "fg_bold_white,bg_bold_red",
            },
        },
        "django.server": {
            "()": ColoredFormatter,
            "format": "%(log_color)s%(message)s",
            "log_colors": {
                "INFO": "bold_black",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "django.server": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
    },
    "root": {
        "handlers": ["console"],
    },
    "loggers": {
        "django": {
            "level": "INFO",
        },
        "django.server": {
            "level": "INFO",
            "handlers": ["django.server"],
            "propagate": False,
        },
        "zds": {
            "level": "INFO",
        },
    },
}

ZDS_APP["site"]["url"] = "http://127.0.0.1:8000"
ZDS_APP["site"]["dns"] = "127.0.0.1:8000"

ZDS_APP["very_top_banner"] = {
    "background_color": "#666",
    "border_color": "#353535",
    "color": "white",
    "message": "Version locale",
    "slug": "version-locale",
}

# --- Celery ---
# Broker : RabbitMQ (docker-compose.rabbit.yml), identifiants lus dans le .env.
# Résultats : base Django (django-celery-results). Le backend rpc:// ne renvoie le résultat
# qu'au client qui a lancé la tâche, donc /result/<id>/ appelé depuis une autre requête
# ne le verrait pas de façon fiable.


def env_required(name):
    """Pas de valeur par défaut silencieuse : on échoue clairement si la variable manque."""
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"{name} manquant dans .env (copier .env.example)")
    return value


QUEUE_HOST = os.environ.get("QUEUE_HOST", "localhost")
CELERY_BROKER_URL = (
    f"amqp://{quote(env_required('RABBITMQ_USER'), safe='')}:{quote(env_required('PASSWORD'), safe='')}"
    f"@{QUEUE_HOST}:{os.environ.get('QUEUE_PORT', '5672')}//"
)
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True  # garde nom de la tâche, args... (visibles dans l'admin)
CELERY_TASK_TRACK_STARTED = True  # état STARTED pendant l'exécution
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
EAGER = os.environ.get("TASKS_EAGER") == "1"  # tests sans broker
CELERY_TASK_ALWAYS_EAGER = EAGER
CELERY_TASK_STORE_EAGER_RESULT = EAGER
CELERY_BEAT_SCHEDULE = {
    "heartbeat-1min": {"task": "polls.tasks.heartbeat", "schedule": crontab(minute="*")},
}
