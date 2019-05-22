# -*- coding: utf-8 -*-
# created by inhzus

from berater.utils.wechat_sdk import AccessToken, Url, Communicate
from berater.config import config, MENU
import json


def create_menu():
    token = AccessToken.get(config[0].API_KEY, config[0].API_SECRET)
    if token:
        url = Url.create_menu.format(access_token=token)
        data = json.dumps(MENU, ensure_ascii=False).encode('utf-8')
        return 'errcode' in Communicate.post(url, data=data)
    return False


if __name__ == '__main__':
    print('Menu create' if create_menu() else 'Menu create failed')
