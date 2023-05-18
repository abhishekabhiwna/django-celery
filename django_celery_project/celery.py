from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

#environment setup, this ensures that celery uses the correct django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_celery_project.settings")

#Creates a new Celery application instance with the name 'django_celery_project'.
app = Celery('django_celery_project')

# Disables the automatic conversion of times to UTC in Celery. It ensures that Celery tasks use the timezone specified in the Django settings.
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

#Loads the Celery configuration from the Django project's settings module. It looks for settings prefixed with CELERY_
app.config_from_object(settings, namespace='CELERY')

#celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-every-day-at-8':{
        'task':'send_mail_app.tasks.send_mail_func',
        'schedule': crontab(hour=8, minute=0),
       
    }
}



#Discovers and registers Celery tasks defined in the Django project. It searches for tasks in any tasks.py files located within the project's installed applications.
app.autodiscover_tasks()



"""
@app.task(bind=True): Decorates the debug_task function as a Celery task. The bind=True argument allows the task to access its own context, including the request 
information.
def debug_task(self): Defines the debug_task function, which simply prints the representation of the task's request."""
@app.task(bind=True)
def debug_task(self):
    print( f'request:{self.request!r}')




#celery -A django_celery_project.celery worker --pool=solo -l info
#celery -A django_celery_project  beat -l info

