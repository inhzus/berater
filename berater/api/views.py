# -*- coding: utf-8 -*-
# created by inhzus

import random

import requests as rq
from flask import Blueprint, request, current_app
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError, NotFound, Conflict

from berater.misc import Response, CandidateTable, StudentTable, Transaction
from berater.utils import token_required, get_crypto_token, current_identity, MemoryCache
from .utils import get_openid_by_code, send_verify_code

api = Blueprint('api', __name__)

code_cache = MemoryCache('code', 60 * 60)


@api.route('/ems')
@token_required
def ems_logistics():
    no = request.args.get('no', '')
    if not no:
        raise BadRequest('Request args \"no\" missing')
    header = {'Authorization': 'APPCODE {}'.format(current_app.config['EXPRESS_APP_CODE'])}
    resp = rq.get(current_app.config['EXPRESS_API_URL'], params={'no': no}, headers=header).json()
    if resp.get('msg', '') != 'ok':
        raise InternalServerError('Get express info failed')
    return Response(**resp.get('result')).json()


@api.route('/token', methods=['POST'])
def get_token():
    openid = get_openid_by_code(request.json.get('code', ''))
    if not openid:
        raise Unauthorized('Code invalid')
    return Response(token=get_crypto_token(openid)).json()


@api.route('/token', methods=['PUT'])
@token_required
def refresh_token():
    return Response(token=get_crypto_token(current_identity)).json()


@api.route('/token', methods=['GET'])
@token_required
def check_token():
    return Response().json()


# Test API: get token
@api.route('/test/token', methods=['GET'])
def test_token():
    return get_crypto_token('test')


@api.route('/code', methods=['POST'])
@token_required
def send_code():
    phone = request.json.get('phone', '')
    if not phone:
        raise BadRequest("Request arg \"phone\" missing")
    gen_code = str(random.randrange(1000, 9999))
    if not send_verify_code(phone, gen_code):
        raise InternalServerError("Send verify code failed")
    code_cache.set(current_identity, code=gen_code, phone=phone)
    return Response().json()


@api.route('/code/<input_code>', methods=['GET'])
@token_required
def check_code(input_code):
    cached = code_cache.get(current_identity)
    if cached.get('code', '') != input_code:
        raise NotFound()
    cached.setdefault('status', 1)
    code_cache.set(current_identity, **cached)
    return Response().json()


@api.route('/candidate', methods=['POST'])
@token_required
def candidate_signup():
    cached = code_cache.get(current_identity)
    if not cached.get('status', False):
        raise Unauthorized('Phone not verified')
    param_keys = ['name', 'province', 'city', 'score']
    params = {k: request.json.get(k) for k in param_keys if k in request.json}
    if len(params.keys()) != 4:
        raise BadRequest('Require params: {}, only get {}'.format(
            ', '.join(param_keys), ', '.join(params.keys())))
    candidate = CandidateTable(openid=current_identity, phone=cached.get('phone'), **params)
    with Transaction() as session:
        if session.query(CandidateTable).filter(CandidateTable.openid == current_identity).first():
            raise Conflict('Candidate has been posted')
        session.add(candidate)
    return Response().json()


@api.route('/candidate', methods=['PATCH'])
@token_required
def candidate_update():
    expected = ['phone', 'name', 'province', 'city', 'score']
    params = {k: request.json.get(k) for k in expected if k in request.json}
    if 'phone' in params:
        cached = code_cache.get(current_identity)
        if not cached.get('status', False):
            raise Unauthorized('Phone not verified')
    with Transaction() as session:
        query = session.query(CandidateTable).filter(CandidateTable.openid == current_identity)
        if not query.first():
            raise NotFound('Candidate not posted')
        query.update(params)
    return Response().json()


@api.route('/student', methods=['POST'])
@token_required
def student_signup():
    cached = code_cache.get(current_identity)
    if not cached.get('status', False):
        raise Unauthorized('Phone not verified')
    expected = ['id_card', 'admission_id', 'student_id']
    params = {k: request.json.get(k) for k in expected if k in request.json}
    keys = params.keys()
    if not (expected[0] in keys and (expected[1] in keys or expected[2] in keys)):
        raise BadRequest('Require params: {}, {} or {}, only get {}'
                         .format(*expected, ', '.join(keys)))
    student = StudentTable(openid=current_identity, phone=cached.get('phone'), **params)
    with Transaction() as session:
        if session.query(StudentTable).filter(StudentTable.openid == current_identity).first():
            raise Conflict('Student has been posted')
        session.add(student)
    return Response().json()
