# -*- coding: utf-8 -*-
# created by inhzus

import hashlib
from time import time
from xml.etree import ElementTree

import requests as rq
from flask import Blueprint, request, make_response, current_app

from berater.misc import Response
from berater.utils.wechat_sdk import MsgFormat

from .bert import candidate_answer

chat = Blueprint('chat', __name__)


@chat.route('/test')
def test_route():
    data = {'code': request.args.get('code', '')}
    resp = rq.post('{}/api/token'.format(
        current_app.config['LOCAL_URL']),
        json=data
    ).json()

    return Response(**resp).json()


@chat.route('/', methods=['GET', 'POST'])
def wechat_msg():
    if 'echostr' in request.args:
        return request.args['echostr']
    data = request.data
    if data:
        msg = {}
        for item in ElementTree.fromstring(data):
            msg[item.tag] = item.text
        if verification():
            answer = candidate_answer(msg['Content'])
            reply = MsgFormat.text % (msg['FromUserName'], msg['ToUserName'], str(time()), answer)
            response = make_response(reply)
            response.content_type = 'application/xml'
            return response
    return "Hello"


def verification() -> bool:
    token = current_app.config['WECHAT_TOKEN']
    args = request.args
    signature = args.get('signature', '')
    timestamp = args.get('timestamp', '')
    nonce = args.get('nonce', '')
    s = ''.join(sorted([timestamp, token, nonce]))
    return hashlib.sha1(s.encode('utf-8')).hexdigest() == signature
