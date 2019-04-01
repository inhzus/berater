# -*- coding: utf-8 -*-
# created by inhzus

import hashlib
from xml.etree import ElementTree
from time import time

from flask import Blueprint, request, make_response
from berater.utils.wechat_sdk import MsgFormat

chat = Blueprint('chat', __name__, url_prefix='/chat')


@chat.route('/')
def wechat_msg():
    data = request.data
    if data:
        msg = {}
        for item in ElementTree.fromstring(data):
            msg[item.tag] = item.text
        if verification():
            reply = MsgFormat.text % (msg['FromUserName'], msg['ToUserName'], str(time()), '')
            response = make_response(reply)
            response.content_type = 'application/xml'
            return response
    return "Hello"


def verification() -> bool:
    token = ''
    args = request.args
    signature = args.get('signature', '')
    timestamp = args.get('timestamp', '')
    nonce = args.get('nonce', '')
    s = ''.join(sorted([timestamp, token, nonce]))
    return hashlib.sha1(s.encode('utf-8')).hexdigest() == signature
