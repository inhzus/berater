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
