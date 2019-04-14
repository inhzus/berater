# -*- coding: utf-8 -*-
# created by inhzus


from berater.utils.wechat_sdk import Url
# noinspection PyUnresolvedReferences
from .secret import (API_KEY, API_SECRET)


class BaseConfig(object):
    PROJECT = 'Berater'
    WECHAT_TOKEN = 'bkzs'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SERVER_URL = 'http://weixinbak.njunova.com'
    # noinspection SpellCheckingInspection
    CRYPTO_KEY = b'ha0jkDDbnn9PT0UKCz1eCZjhVvCVwYWpaG5x2T_P1xo='


class ProductionConfig(BaseConfig):
    pass


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig
}

MENU = {
    'button': {
        {
            'type': 'view',
            'name': '测试按钮',
            'url': Url.oauth2_auth_token.format(
                appid=API_KEY,
                redirect_url='{}/chat/test'.format(DevelopmentConfig.SERVER_URL))
        }
    }
}
