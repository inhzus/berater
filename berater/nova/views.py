# -*- coding: utf-8 -*-
# created by inhzus

from typing import List

from flask import Blueprint, request
from werkzeug.exceptions import NotFound, Conflict, BadRequest

from berater.misc import Transaction, NovaRegTable, Response, StudentTable, SourceStudentTable
from berater.utils import token_required, current_identity, Permission

nova = Blueprint('nova', __name__)


@nova.route('/source', methods=['GET'])
@token_required()
def get_source():
    with Transaction() as session:
        student: StudentTable = session.query(StudentTable).filter(
            StudentTable.openid == current_identity.openid).first()
        assert student is not None
        phone = student.phone
        source: SourceStudentTable = session.query(SourceStudentTable).filter(
            SourceStudentTable.id_card == student.id_card
        ).first()
        assert source is not None
        return Response(stuid=source.stuid, name=source.name, department=source.department, phone=phone).json()


@nova.route('/info', methods=['GET'])
@token_required()
def get_info():
    with Transaction() as session:
        reg: NovaRegTable = session.query(NovaRegTable).filter(
            NovaRegTable.openid == current_identity.openid
        ).first()
        if not reg:
            raise NotFound('student not registered')
        return Response(**reg.to_dict()).json()


@nova.route('/info', methods=['POST'])
@token_required()
def post_info():
    param_keys = [m.key for m in NovaRegTable.__table__.columns]
    param_keys.remove('openid')
    params = {k: request.json.get(k) for k in param_keys if k in request.json}
    if len(param_keys) != len(params):
        raise BadRequest('Require params: {}, only get: {}'.format(
            ', '.join(param_keys), ', '.join(params.keys())))
    reg: NovaRegTable = NovaRegTable(openid=current_identity.openid, **params)
    with Transaction() as session:
        if session.query(NovaRegTable).filter(NovaRegTable.openid == current_identity.openid).first():
            raise Conflict('student registered before')
        session.add(reg)
    return Response().json()


@nova.route('/info', methods=['DELETE'])
@token_required()
def cancel_register():
    with Transaction() as session:
        reg: NovaRegTable = session.query(NovaRegTable).filter(
            NovaRegTable.openid == current_identity.openid
        ).first()
        if not reg:
            raise NotFound('student not registered')
        session.delete(reg)
        return Response().json()


@nova.route('/admin/info', methods=['GET'])
@token_required(Permission.NOVA_ADMIN)
def admin_get_info():
    with Transaction() as session:
        regs: List[NovaRegTable] = session.query(NovaRegTable).all()
        return Response(students=[reg.to_dict() for reg in regs]).json()
