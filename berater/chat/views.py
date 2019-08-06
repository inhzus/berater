# -*- coding: utf-8 -*-
# created by inhzus

import hashlib
from time import time
from xml.etree import ElementTree

import requests as rq
from flask import Blueprint, request, make_response, current_app

from berater.misc import Response, Transaction, StudentTable, SourceStudentTable
from berater.utils import current_identity
from berater.utils.wechat_sdk import MsgFormat

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
            content = 'Developing'
            if msg['Event'] == 'CLICK':
                content = '请先点击其他任一功能进行信息绑定'
                with Transaction() as session:
                    student: StudentTable = session.query(StudentTable).filter(
                        StudentTable.openid == msg['FromUserName']).first()
                    if student:
                        source_student: SourceStudentTable = session.query(
                            SourceStudentTable.stuid, SourceStudentTable.admission_id
                        ).filter(SourceStudentTable.id_card == student.id_card).first()
                        if source_student:
                            content = '学号: {}'.format(source_student.stuid)
            reply = MsgFormat.text % (msg['FromUserName'], msg['ToUserName'], str(time()), content)
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
