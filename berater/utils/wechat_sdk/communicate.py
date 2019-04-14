# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
"""

import requests


class Communicate(object):
    """
    此类只为与API 交互时能更方便地获得其json()
    """
    @staticmethod
    def get(url: str, **kwargs) -> dict:
        ret = requests.get(url, **kwargs)
        return ret.json()

    @staticmethod
    def post(url: str, data=None, **kwargs) -> dict:
        return requests.post(url, data, **kwargs).json()
