# -*- coding: utf-8 -*-
"""
Created by suun on 5/17/2018
"""
from .communicate import Communicate
from .token import AccessToken
from .url import Url


def send_template_msg(appid, secret, data):
    access_token = AccessToken.get(appid, secret)
    url = Url.send_template_msg.format(access_token=access_token)
    return Communicate.post(url, data.encode('utf-8'))
