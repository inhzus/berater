# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint, request

from berater.exception import UnauthorizedException
from berater.misc import Response
from berater.utils import token_required, get_crypto_token, current_identity
from .wechat import get_openid_by_code

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/info')
def update_info():
    pass


@api.route('/ems')
def ems_logistics():
    pass


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
