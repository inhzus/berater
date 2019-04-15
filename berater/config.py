# -*- coding: utf-8 -*-
# created by inhzus


from berater.utils.wechat_sdk import Url


class BaseConfig(object):
    config_name = ''
    PROJECT = 'Berater'
    WECHAT_TOKEN = 'bkzs'
    EXPRESS_API_URL = 'http://kdwlcxf.market.alicloudapi.com/kdwlcx'
    # noinspection PyUnresolvedReferences
    from .secret import (API_KEY, API_SECRET, EXPRESS_APP_CODE)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SERVER_URL = 'http://weixinbak.njunova.com'
    LOCAL_URL = 'http://localhost:5000'
    # noinspection SpellCheckingInspection
    CRYPTO_KEY = b'ha0jkDDbnn9PT0UKCz1eCZjhVvCVwYWpaG5x2T_P1xo='


class ProductionConfig(BaseConfig):
    pass


config = {
    'dev': DevelopmentConfig,
    'pro': ProductionConfig,
    0: DevelopmentConfig
}

MENU = {
    'button': [
        {
            'type': 'view',
            'name': '测试按钮',
            'url': Url.oauth2_new_page.format(
                appid=config[0].API_KEY,
                redirect_url='{}/chat/test'.format(DevelopmentConfig.SERVER_URL))
        }
    ]
}
