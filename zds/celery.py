import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zds.settings.dev")

app = Celery("zds")

# Toutes les options Celery sont lues dans les settings Django, préfixées par CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Découvre automatiquement les modules `tasks.py` de chaque app installée
app.autodiscover_tasks()
