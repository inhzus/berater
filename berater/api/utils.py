# -*- coding: utf-8 -*-
# created by inhzus


# from berater.config import API_KEY, API_SECRET
from berater.config import config
from berater.utils import wechat_sdk, AliSMS

_sms = AliSMS(config[0].SMS_ACCESS_KEY, config[0].SMS_ACCESS_SECRET, config[0].SMS_SIGN_NAME)


def send_verify_code(phone_number, verify_code) -> bool:
    params = {
        'code': verify_code
    }
    ret = _sms.send(phone_number, config[0].SMS_TEMPLATE_CODE, params).json()
    return 'Code' in ret and ret['Code'] == 'OK'


def get_openid_by_code(code: str):
    return wechat_sdk.get_openid_from_code(code, config[0].API_KEY, config[0].API_SECRET)
