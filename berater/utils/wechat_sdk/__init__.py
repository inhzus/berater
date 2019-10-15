# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
对微信服务号API 的简单封装
"""
from .communicate import Communicate
from .openid import get_openid_from_code
from .res_format import MsgFormat, TemplateFormat
from .token import get_access_token_directly
from .url import Url

__author__ = 'Zhi Sun'
__version__ = '0.2'
