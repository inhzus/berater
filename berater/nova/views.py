# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint, request
from werkzeug.exceptions import NotFound, Conflict, BadRequest

from berater.utils import token_required, current_identity
from berater.misc import Transaction, NovaRegTable, Response

nova = Blueprint('nova', __name__)


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
