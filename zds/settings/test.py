from .abstract_base import *
from .abstract_test import *

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp/django_cache",
    }
}
CELERY_TASK_ALWAYS_EAGER = True  # les tâches s'exécutent en direct, sans broker
CELERY_TASK_EAGER_PROPAGATES = True  # une exception dans une tâche fait échouer le test
