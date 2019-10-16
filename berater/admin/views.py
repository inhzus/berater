# -*- coding: utf-8 -*-
# created by inhzus

import uuid
from urllib.parse import quote

from flask import Blueprint, current_app, request, url_for, redirect
from werkzeug.exceptions import BadRequest, Conflict, NotFound, Unauthorized

from berater.misc import Response, MemoryCache, PrivilegeTable, Transaction, get_roles_of_openid
from berater.utils import Permission
from berater.utils.wechat_sdk import Url, get_openid_from_code

admin = Blueprint('admin', __name__)
link_cache = MemoryCache('link', 30 * 60)


def gen_redirect_url(url: str) -> str:
    return Url.oauth2_new_page.format(
        appid=current_app.config['API_KEY'],
        redirect_url=quote(url)
    )


def get_openid(code: str) -> str:
    return get_openid_from_code(code, current_app.config['API_KEY'], current_app.config['API_SECRET'])


@admin.route('/go/link/<string:role>')
def go_gen_link(role):
    return redirect(gen_redirect_url(format(current_app.config['SERVER_URL'] + url_for('admin.gen_link', role=role))))


@admin.route('/link/<string:role>')
def gen_link(role):
    openid = get_openid(request.args.get('code', ''))
    if not openid:
        raise Unauthorized('code invalid')
    if Permission.ADMIN not in get_roles_of_openid(openid):
        raise Unauthorized('admin privilege need')
    if Permission.loads(role) == Permission.EMPTY:
        return BadRequest('unknown role')
    seq = uuid.uuid4().hex
    link_cache.set(seq, role=role)
    link = '{}{}?seq={}'.format(current_app.config['SERVER_URL'], url_for('admin.auth'), seq)
    return Response(link=gen_redirect_url(link)).json()


@admin.route('/auth')
def auth():
    openid = get_openid(request.args.get('code', ''))
    if not openid:
        raise Unauthorized('code invalid')
    seq = request.args.get('seq', '')
    if not seq:
        raise BadRequest('seq empty')
    cached = link_cache.get(seq)
    role = cached.get('role', '')
    if not role:
        return NotFound('link invalid')
    permission = Permission.loads(role)
    privilege = PrivilegeTable(openid=openid, permission=permission.value)
    with Transaction() as session:
        if session.query(PrivilegeTable).filter_by(openid=openid, permission=permission.value).first():
            return Conflict('privilege has been checked before')
        session.add(privilege)
    return Response().json()
