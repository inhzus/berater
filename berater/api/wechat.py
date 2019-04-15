# -*- coding: utf-8 -*-
# created by inhzus


from berater.utils import wechat_sdk
# from berater.config import API_KEY, API_SECRET
from berater.config import config


def get_openid_by_code(code: str):
    return wechat_sdk.get_openid_from_code(code, config[0].API_KEY, config[0].API_SECRET)
