# -*- coding: utf-8 -*-
# created by inhzus

from os import getenv

import requests


# noinspection SpellCheckingInspection
def send_serer_chan_msg(title: str, desc: str = ''):
    key = getenv('SCKEY')
    url = f'https://sc.ftqq.com/{key}.send'
    print(url)
    print(requests.post(url, data={
        'text': title,
        'desp': desc
    }).content.decode('utf-8'))
