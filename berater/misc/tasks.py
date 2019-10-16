# -*- coding: utf-8 -*-
# created by inhzus

from os import getenv

from celery import Celery
from celery.schedules import crontab

from berater.utils.wechat_sdk import get_access_token_directly
from .cache import MemoryCache

token_cache = MemoryCache('access_token', 7200)

cron = Celery(
    'tasks',
    broker=getenv('CELERY_BROKER_URL', 'redis://redis:6379/1'),
    backend=getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/1'))


@cron.on_after_configure.connect
def setup_periodic_tasks(**_):
    cron.add_periodic_task(crontab(minute='0', hour='*'), refresh_access_token.s())


@cron.task(bind=True, max_retries=3)
def refresh_access_token(self):
    token, errmsg = get_access_token_directly(getenv('API_KEY'), getenv('API_SECRET'))
    print(f'token: {token}; {errmsg}')
    # noinspection PyBroadException
    try:
        if errmsg or not token:
            raise Exception(errmsg)
        token_cache.set('', token=token)
        return token
    except Exception:
        return self.retry(countdown=5)
