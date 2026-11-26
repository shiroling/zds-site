import os

from django.core.exceptions import ImproperlyConfigured

from .django import TIME_ZONE

celery_config = {"user": "admin", "pass": "changeme", "port": "5672", "managment_port": "15672"}


def env_required(name):
    """Pas de valeur par défaut silencieuse : on échoue clairement si la variable manque."""
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"{name} manquant dans .env (copier .env.example)")
    return value


QUEUE_HOST = os.environ.get("QUEUE_HOST", "localhost")
CELERY_BROKER_URL = f"amqp://{celery_config['user']}:{celery_config['pass']}" f"@{QUEUE_HOST}:{celery_config['port']}//"

CELERY_TASK_IGNORE_RESULT = True  # pas de result backend
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

CELERY_TASK_ACKS_LATE = True  # le message n'est acquitté qu'après exécution
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # un worker ne réserve pas plusieurs PDF d'avance

CELERY_TASK_DEFAULT_QUEUE = "default"
