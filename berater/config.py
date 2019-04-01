# -*- coding: utf-8 -*-
# created by inhzus


class BaseConfig(object):
    PROJECT = 'Berater'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    pass


class ProductionConfig(BaseConfig):
    pass


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}
