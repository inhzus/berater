# -*- coding: utf-8 -*-
# created by inhzus

from os import getenv
from time import asctime

from celery import Celery
from celery.exceptions import MaxRetriesExceededError
from celery.schedules import crontab
from celery.signals import after_setup_logger

from berater.utils import send_server_chan_msg, get_file_log_handler
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


@after_setup_logger.connect()
def logger_setup_handler(logger, **_):
    handler = get_file_log_handler('log/celery.log')
    logger.addHandler(handler)
    logger.info("My log handler connected -> Global Logging")


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
        try:
            return self.retry(countdown=5)
        except MaxRetriesExceededError as e:
            send_server_chan_msg('Celery服务', f'Celery task (refresh_access_token) triggered max retries at {asctime()}')
            raise e
