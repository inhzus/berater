# -*- coding: utf-8 -*-
# created by inhzus


# noinspection PyUnresolvedReferences
from .secret import (API_KEY, API_SECRET)


class BaseConfig(object):
    PROJECT = 'Berater'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # noinspection SpellCheckingInspection
    CRYPTO_KEY = b'ha0jkDDbnn9PT0UKCz1eCZjhVvCVwYWpaG5x2T_P1xo='


class ProductionConfig(BaseConfig):
    pass


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}
