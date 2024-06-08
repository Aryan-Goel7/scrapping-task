import os 
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainProject.settings')

class celery_app:
    def __init__(self):
        self.app = Celery("mainProject")
        self.app.config_from_object("django.conf:settings" , namespace="CELERY")


celery_app_instance = celery_app()
app = celery_app_instance.app

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')