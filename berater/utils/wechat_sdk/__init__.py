# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
对微信服务号API 的简单封装
"""
from .communicate import Communicate
from .exceptions import WechatException
from .openid import get_openid_from_code
from .res_format import MsgFormat, TemplateFormat
from .sender import send_template_msg
from .token import AccessToken
from .url import Url

__author__ = 'Zhi Sun'
__version__ = '0.1'
__all__ = {
    'MsgFormat',
    'Url',
    'AccessToken',
    'Communicate',
    'TemplateFormat',
    'WechatException',
    'send_template_msg',
    'get_openid_from_code'
}
