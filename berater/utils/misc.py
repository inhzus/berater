# -*- coding: utf-8 -*-
# created by inhzus
from typing import List

from berater.misc import Transaction, PrivilegeTable, StudentTable, CandidateTable, MemoryCache
from berater.utils import Permission, gen_token
from berater.utils.wechat_sdk import Url, Communicate

token_cache = MemoryCache('access_token', 7200)


def send_template_msg(data):
    access_token = get_access_token()
    url = Url.send_template_msg.format(access_token=access_token)
    return Communicate.post(url, data.encode('utf-8'))


def get_roles_of_openid(openid: str) -> List[Permission]:
    roles = []
    with Transaction() as session:
        privileges: List[PrivilegeTable] = session.query(PrivilegeTable).filter(PrivilegeTable.openid == openid).all()
        for privilege in privileges:
            roles.append(Permission(privilege.permission))
        if session.query(StudentTable).filter(StudentTable.openid == openid).first():
            roles.append(Permission.STUDENT)
        if session.query(CandidateTable).filter(CandidateTable.openid == openid).first():
            roles.append(Permission.CANDIDATE)
    return roles


def get_crypto_token(openid: str) -> str:
    return gen_token(openid, get_roles_of_openid(openid))


def get_access_token() -> str:
    return token_cache.get('').get('token', '')
