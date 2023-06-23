from __future__ import absolute_import, unicode_literals

from celery.schedules import crontab
from celery.task import periodic_task
from datetime import timedelta

@periodic_task(run_every=timedelta(seconds=5))
def every_monday_morning():
    print("This is run every 30s")