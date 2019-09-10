# -*- coding: utf-8 -*-
# created by inhzus

import random

import requests as rq
from flask import Blueprint, request, current_app
from sqlalchemy import and_, or_
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError, NotFound, Conflict

from berater.api.utils import get_openid_by_code, send_verify_code
from berater.misc import Response, CandidateTable, StudentTable, SourceStudentTable, Transaction
from berater.utils import (token_required, current_identity, get_crypto_token,
                           MemoryCache, candidate_answer, tf_idf_client)

api = Blueprint('api', __name__)

code_cache = MemoryCache('code', 60 * 60)


@api.route('/ems')
@token_required()
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
    with Transaction() as session:
        is_candidate = True if session.query(CandidateTable).filter(CandidateTable.openid == openid).first() else False
        is_student = True if session.query(StudentTable).filter(StudentTable.openid == openid).first() else False
    return Response(token=get_crypto_token(openid), candidate=is_candidate, student=is_student).json()


@api.route('/token', methods=['PUT'])
@token_required()
def refresh_token():
    return Response(token=get_crypto_token(current_identity.openid)).json()


@api.route('/token', methods=['GET'])
@token_required()
def check_token():
    with Transaction() as session:
        student: StudentTable = session.query(StudentTable).filter(
            StudentTable.openid == current_identity.openid).first()
        admission_id = stuid = ''
        if student:
            source_student: SourceStudentTable = session.query(
                SourceStudentTable.stuid, SourceStudentTable.admission_id
            ).filter(SourceStudentTable.id_card == student.id_card).first()
            if source_student:
                stuid = source_student.stuid
                admission_id = source_student.admission_id
    return Response(stuid=stuid, admission_id=admission_id).json()


# Test API: get token
@api.route('/test/token/<openid>', methods=['POST'])
def test_token(openid):
    with Transaction() as session:
        is_candidate = True if session.query(CandidateTable).filter(CandidateTable.openid == openid).first() else False
        is_student = True if session.query(StudentTable).filter(StudentTable.openid == openid).first() else False
    return Response(token=get_crypto_token(openid), candidate=is_candidate, student=is_student).json()


@api.route('/code', methods=['POST'])
@token_required()
def send_code():
    phone = request.json.get('phone', '')
    if not phone:
        raise BadRequest('Request arg \"phone\" missing')
    gen_code = str(random.randrange(1000, 9999))
    status, msg = send_verify_code(phone, gen_code)
    if not status:
        raise InternalServerError(msg)
    code_cache.set(current_identity.openid, code=gen_code, phone=phone)
    return Response().json()


@api.route('/code/<input_code>', methods=['GET'])
@token_required()
def check_code(input_code):
    cached = code_cache.get(current_identity.openid)
    if cached.get('code', '') != input_code:
        raise NotFound()
    cached.setdefault('status', 1)
    code_cache.set(current_identity.openid, **cached)
    return Response().json()


@api.route('/candidate', methods=['POST'])
@token_required()
def candidate_signup():
    cached = code_cache.get(current_identity.openid)
    if not cached.get('status', False):
        raise Unauthorized('Phone not verified')
    param_keys = ['name', 'province', 'city', 'score', 'subject']
    params = {k: request.json.get(k) for k in param_keys if k in request.json}
    if len(params.keys()) != len(param_keys):
        raise BadRequest('Require params: {}, only get {}'.format(
            ', '.join(param_keys), ', '.join(params.keys())))
    candidate = CandidateTable(openid=current_identity.openid, phone=cached.get('phone'), **params)
    with Transaction() as session:
        if session.query(CandidateTable).filter(CandidateTable.openid == current_identity.openid).first():
            raise Conflict('Candidate has been posted')
        session.add(candidate)
    return Response().json()


@api.route('/candidate', methods=['PATCH'])
@token_required()
def candidate_update():
    expected = ['phone', 'name', 'province', 'city', 'score', 'subject']
    params = {k: request.json.get(k) for k in expected if k in request.json}
    with Transaction() as session:
        query = session.query(CandidateTable).filter(CandidateTable.openid == current_identity.openid)
        candidate: CandidateTable = query.first()
        if not candidate:
            raise NotFound('Candidate not posted')
        if candidate.phone != params.get('phone', candidate.phone):
            cached = code_cache.get(current_identity.openid)
            if not cached.get('status', False):
                raise Unauthorized('Phone not verified')
        query.update(params)
    return Response().json()


@api.route('/student', methods=['POST'])
@token_required()
def student_signup():
    cached = code_cache.get(current_identity.openid)
    if not cached.get('status', False):
        raise Unauthorized('Phone not verified')
    expected = ['id_card', 'id']
    params = {k: request.json.get(k) for k in expected if k in request.json}
    keys = params.keys()
    if len(keys) != len(expected):
        raise BadRequest('Require params: {}, only get {}'
                         .format(', '.join(expected), ', '.join(keys)))
    student = StudentTable(openid=current_identity.openid, phone=cached.get('phone'), id_card=params.get('id_card'))
    with Transaction() as session:
        if not session.query(SourceStudentTable).filter(
                and_(SourceStudentTable.id_card == params.get('id_card'),
                     or_(SourceStudentTable.admission_id == params.get('id'),
                         SourceStudentTable.stuid == params.get('id')))).first():
            raise NotFound('Correspond id of id_card not found')
        if session.query(StudentTable).filter(StudentTable.openid == current_identity.openid).first():
            raise Conflict('Student has been posted')
        session.add(student)
    return Response().json()


@api.route('/student', methods=['PATCH'])
@token_required()
def student_update():
    expected = ['phone', 'id_card', 'admission_id', 'student_id']
    params = {k: request.json.get(k) for k in expected if k in request.json}
    with Transaction() as session:
        query = session.query(StudentTable).filter(StudentTable.openid == current_identity.openid)
        student: StudentTable = query.first()
        if not student:
            raise NotFound('Student not posted')
        if student.phone != params.get('phone', student.phone):
            cached = code_cache.get(current_identity.openid)
            if not cached.get('status', False):
                raise Unauthorized('Phone not verified')
        query.update(params)
    return Response().json()


@api.route('/source', methods=['GET'])
@token_required()
def get_source_student_info():
    with Transaction() as session:
        query = session.query(StudentTable).filter(StudentTable.openid == current_identity.openid)
        student: StudentTable = query.first()
        if not student:
            raise NotFound('Student not registered')
        source: SourceStudentTable = session.query(SourceStudentTable).filter(
            SourceStudentTable.id_card == student.id_card).first()
        if not source:
            raise NotFound('Source student info not found')
        return Response(**source.to_dict()).json()


@api.route('/qna', methods=['GET'])
@token_required()
def qna():
    q = request.args.get('q', '')
    if not q:
        raise BadRequest('Request arg "q" missing')
    answer = '\n\n'.join(tf_idf_client.find_all(q))
    return Response(answer=answer).json()


@api.route('/bert', methods=['GET'])
@token_required()
def bert():
    q = request.args.get('q', '')
    if not q:
        raise BadRequest('Request arg "q" missing')
    answer = candidate_answer(q)
    if answer is None:
        raise InternalServerError('Bert server error')
    # TODO
    # filter = or_(*(QNA.q.like(a) for a in answer[0]))
    # query = engine.session.query(QNA.q, QNA.a).filter(filter)
    # ret = [{'q': row.q, 'a': row.a} for row in query.all()]
    # q_list, a_list = map(ret, zip(*ret))
    ret = [{'q': answer[0][i], 'a': answer[1][i]} for i in range(len(answer[0]))]
    return Response(answer=ret).json()
