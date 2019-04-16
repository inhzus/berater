# -*- coding: utf-8 -*-
# created by inhzus


from berater.utils.wechat_sdk import Url


class BaseConfig(object):
    PROJECT = 'Berater'
    WECHAT_TOKEN = 'bkzs'

    # Ali express API
    EXPRESS_API_URL = 'http://kdwlcxf.market.alicloudapi.com/kdwlcx'

    # Ali short message service
    SMS_SIGN_NAME = '南大咨询'
    SMS_TEMPLATE_CODE = 'SMS_163433313'

    # Flask SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/berater'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 5

    # noinspection PyUnresolvedReferences
    from .secret import (API_KEY, API_SECRET, EXPRESS_APP_CODE, SMS_ACCESS_KEY, SMS_ACCESS_SECRET)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SERVER_URL = 'http://weixinbak.njunova.com'
    LOCAL_URL = 'http://localhost:5000'
    # noinspection SpellCheckingInspection
    CRYPTO_KEY = b'ha0jkDDbnn9PT0UKCz1eCZjhVvCVwYWpaG5x2T_P1xo='

    # Flask SQLAlchemy
    SQLALCHEMY_ECHO = True


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
            'name': '服务号相关功能正在开发',
            'url': Url.oauth2_new_page.format(
                appid=config[0].API_KEY,
                redirect_url='{}/chat/test'.format(DevelopmentConfig.SERVER_URL))
        }
    ]
}
