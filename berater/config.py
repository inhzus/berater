# -*- coding: utf-8 -*-
# created by inhzus


from berater.utils.wechat_sdk import Url
from os import getenv


class BaseConfig(object):
    PROJECT = 'Berater'
    WECHAT_TOKEN = 'bkzs'

    # Ali express API
    EXPRESS_API_URL = 'http://kdwlcxf.market.alicloudapi.com/kdwlcx'

    # Ali short message service
    SMS_SIGN_NAME = '南大咨询'
    SMS_TEMPLATE_CODE = 'SMS_163433313'

    # Flask SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@mysql/{}'.format(
        getenv('MYSQL_USER', ''), getenv('MYSQL_PASSWORD', ''), getenv('MYSQL_DATABASE', ''))
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@mysql/berater'
    SQLALCHEMY_BINDS = {
        'local': SQLALCHEMY_DATABASE_URI
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 5
    APP_TOKEN = {
        'face': getenv('APP_TOKEN_FACE', '')
    }

    # noinspection PyUnresolvedReferences
    API_KEY = getenv('API_KEY', '')
    API_SECRET = getenv('API_SECRET', '')
    EXPRESS_APP_CODE = getenv('EXPRESS_APP_CODE', '')
    SMS_ACCESS_KEY = getenv('SMS_ACCESS_KEY', '')
    SMS_ACCESS_SECRET = getenv('SMS_ACCESS_SECRET', '')
    # from .secret import (API_KEY, API_SECRET, EXPRESS_APP_CODE, SMS_ACCESS_KEY, SMS_ACCESS_SECRET)

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
