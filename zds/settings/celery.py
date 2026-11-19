import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproto.settings")

app = Celery("djangoproto")
# Lit tous les réglages préfixés CELERY_ dans settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")
# Cherche un fichier tasks.py dans chaque app installée
app.autodiscover_tasks()
