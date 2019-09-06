# -*- coding: utf-8 -*-
# created by inhzus
from typing import List

from berater.misc import Transaction, PrivilegeTable
from berater.utils import Permission, gen_token


def get_roles_of_openid(openid: str) -> List[Permission]:
    roles = [Permission.USER]
    with Transaction() as session:
        privileges: List[PrivilegeTable] = session.query(PrivilegeTable).filter(PrivilegeTable.openid == openid).all()
        for privilege in privileges:
            roles.append(Permission(privilege.permission))
    return roles


def get_crypto_token(openid: str) -> str:
    return gen_token(openid, get_roles_of_openid(openid))