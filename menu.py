# -*- coding: utf-8 -*-
# created by inhzus

import json

from redis import Redis

from berater.config import MENU
from berater.misc import MemoryCache
from berater.utils.wechat_sdk import Url, Communicate


def create_menu():
    cli = Redis(port=63790)
    token = cli.get(MemoryCache.concat_keys('', 'access_token'))
    if token:
        url = Url.create_menu.format(access_token=token)
        data = json.dumps(MENU, ensure_ascii=False).encode('utf-8')
        ret = Communicate.post(url, data=data)
        print(ret)
        print(Communicate.get(Url.get_menu.format(access_token=token)))


if __name__ == '__main__':
    create_menu()
