# -*- coding: utf-8 -*-
# created by inhzus

import json

from berater.config import config, MENU
from berater.utils.wechat_sdk import AccessToken, Url, Communicate


def create_menu():
    token = AccessToken.get(config[0].API_KEY, config[0].API_SECRET)
    if token:
        url = Url.create_menu.format(access_token=token)
        data = json.dumps(MENU, ensure_ascii=False).encode('utf-8')
        ret = Communicate.post(url, data=data)
        print(ret)


if __name__ == '__main__':
    create_menu()
