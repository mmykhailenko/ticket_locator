from __future__ import absolute_import, unicode_literals

import time

from celery import shared_task


@shared_task(time_limit=300)
def create_task(number):
    time.sleep(number)
    return 'OK'
