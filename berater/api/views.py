# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint, request, current_app
import requests as rq

from berater.exception import UnauthorizedException, BadRequestException, InternalServerException
from berater.misc import Response
from berater.utils import token_required, get_crypto_token, current_identity, MemoryCache
from .utils import get_openid_by_code, send_verify_code
import random


api = Blueprint('api', __name__, url_prefix='/api')

code_cache = MemoryCache(5 * 60)


@api.route('/info')
def update_info():
    pass


@api.route('/ems')
@token_required
def ems_logistics():
    no = request.args.get('no', '')
    if no:
        header = {
            'Authorization': 'APPCODE {}'.format(current_app.config['EXPRESS_APP_CODE'])
        }
        resp = rq.get(current_app.config['EXPRESS_API_URL'], params={'no': no}, headers=header).json()
        if resp.get('msg', '') == 'ok':
            return Response(**resp.get('result')).json()
        raise InternalServerException('Get express info failed')
    raise BadRequestException('Request args \"no\" missing')


@api.route('/token', methods=['POST'])
def get_token():
    openid = get_openid_by_code(request.json.get('code', ''))
    if not openid:
        raise UnauthorizedException('Code invalid')
    return Response(token=get_crypto_token(openid)).json()


@api.route('/token', methods=['PATCH'])
@token_required
def refresh_token():
    return get_crypto_token(current_identity)


# Test API: get token
@api.route('/token', methods=['GET'])
def test_token():
    return get_crypto_token('test')


@api.route('/code', methods=['POST'])
@token_required
def send_code():
    # phone = request.json.get('phone', '')
    # if phone:
    #     gen_code = random.randrange(1000, 9999)
    #     if send_verify_code(phone, gen_code):
    #
    #     code_cache.set(current_identity, v='test')
    code_cache.set(current_identity, v='test')
    return Response(**code_cache.get(current_identity)).json()


@api.route('/code', methods=['GET'])
@token_required
def get_code():
    code_cache.put(current_identity, v='test2', p='test3')
    return Response(**code_cache.get(current_identity)).json()
