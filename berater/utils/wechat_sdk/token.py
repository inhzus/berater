# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
"""

from .communicate import Communicate
from .url import Url


def get_access_token_directly(appid: str, secret: str) -> (str, str):
    url = Url.token.format(appid=appid, appsecret=secret)
    res = Communicate.get(url)
    if 'errcode' in res:
        return '', res.get('errmsg', '')
        # return {'status': 0, 'errmsg': res.get('errmsg'), 'errcode': res.get('errcode')}
    else:
        return res.get('access_token', ''), ''
