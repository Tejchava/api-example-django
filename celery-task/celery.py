from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drchrono.settings')

app = Celery('drchrono',
             include=['celery-task.tasks'])

# Beat schedule runs at every day morning 9:00Am in UTC timezone
app.conf.CELERYBEAT_SCHEDULE = {
    'auto-mail': {
        'task': 'celery-task.tasks.send_bday_mail',
        'schedule': crontab(minute=0, hour=9),
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

