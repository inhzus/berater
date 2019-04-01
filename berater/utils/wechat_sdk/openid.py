# -*- coding: utf-8 -*-
"""
Created by suun on 5/17/2018
"""

from .communicate import Communicate
from .url import Url


def get_openid_from_code(code, appid, secret):
    """
    根据临时code 得到openid
    :return: 得到openid 则直接返回其值，否则返回None
    """
    url = Url.oauth2_token.format(appid=appid, appsecret=secret, code=code)
    ret = Communicate.get(url)
    # print(ret)
    return ret.get('openid', None)
