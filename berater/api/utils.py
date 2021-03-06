# -*- coding: utf-8 -*-
# created by inhzus

from typing import Tuple

from flask import current_app

# from berater.config import API_KEY, API_SECRET
from berater.config import config
from berater.utils import wechat_sdk, AliSMS

_sms = AliSMS(config[0].SMS_ACCESS_KEY, config[0].SMS_ACCESS_SECRET, config[0].SMS_SIGN_NAME)


def send_verify_code(phone_number: str, verify_code: str) -> Tuple[bool, str]:
    params = {
        'code': verify_code
    }
    ret = _sms.send(phone_number, config[0].SMS_TEMPLATE_CODE, params).json()
    current_app.logger.info('[sms] verify code sent to {}, return {}'.format(verify_code, phone_number, ret))
    status = 'Code' in ret and ret['Code'] == 'OK'
    return status, '' if status else ret['Message']


def get_openid_by_code(code: str) -> str:
    return wechat_sdk.get_openid_from_code(code, config[0].API_KEY, config[0].API_SECRET)
