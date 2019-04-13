# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint
from berater.utils import token_required, get_crypto_token, current_identity

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/info')
def update_info():
    pass


@api.route('/ems')
def ems_logistics():
    pass


@api.route('/token', methods=['POST'])
def get_token():
    openid = 'test'
    return get_crypto_token(openid)


@api.route('/token', methods=['PATCH'])
@token_required
def refresh_token():
    return get_crypto_token(current_identity)
