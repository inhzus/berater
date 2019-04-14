# -*- coding: utf-8 -*-
# created by inhzus


from berater.utils import wechat_sdk
from berater.config import API_KEY, API_SECRET


def get_openid_by_code(code: str):
    return wechat_sdk.get_openid_from_code(code, API_KEY, API_SECRET)
