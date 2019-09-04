# -*- coding: utf-8 -*-
# created by inhzus

import json
from enum import Enum
from functools import wraps
from typing import List

from cryptography.fernet import Fernet, InvalidToken
# noinspection PyProtectedMember
from flask import current_app, _request_ctx_stack, request
from werkzeug.exceptions import Unauthorized
from werkzeug.local import LocalProxy

CONFIG_DEFAULTS = {
    'CRYPTO_TTL': 60 * 60,
    'CRYPTO_HEADER_KEY': 'Authorization',
    'CRYPTO_KEY': Fernet.generate_key()
}


class Permission(Enum):
    EMPTY = 0
    USER = 1
    FACE = 2
    NOVA_ADMIN = 3

    @staticmethod
    def loads(s: str) -> 'Permission':
        d = {
            'face': Permission.FACE,
            'user': Permission.USER,
            'nova_admin': Permission.NOVA_ADMIN
        }
        return d.get(s, Permission.EMPTY)


class User:
    @staticmethod
    def default_roles():
        return [Permission.USER]

    def __init__(self, openid, roles: List[Permission] = None):
        self.openid = openid
        self.roles = roles
        if roles is None:
            self.roles = [Permission.USER]

    def dumps(self):
        return json.dumps({"openid": self.openid, "roles": [role.value for role in self.roles]})

    @staticmethod
    def loads(data):
        d = json.loads(data)
        u = User(openid=d["openid"], roles=[Permission(role) for role in d["roles"]])
        return u


class Crypto:
    def __init__(self, app=None):
        # noinspection PyTypeChecker
        self.fer: Fernet = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in CONFIG_DEFAULTS.items():
            app.config.setdefault(k, v)
        self.fer = Fernet(app.config['CRYPTO_KEY'].encode())
        app.extensions['crypto'] = self

    def encrypt(self, data: str):
        return self.fer.encrypt(data.encode()).decode()

    def decrypt(self, data: str):
        return self.fer.decrypt(data.encode(), current_app.config['CRYPTO_TTL'])


_crypto = LocalProxy(lambda: current_app.extensions['crypto'])
# noinspection PyTypeChecker
current_identity: User = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_identity', None))


def _token_required(role: Permission):
    authorization_list: List[str] = request.headers.get(current_app.config['CRYPTO_HEADER_KEY'], '').split(' ')
    if len(authorization_list) < 2:
        raise Unauthorized('Token not in request headers')
    elif len(authorization_list) == 3:
        app_name = authorization_list[1]
        token = authorization_list[2]
        app_token: dict = current_app.config['APP_TOKEN']
        if app_token.get(app_name, '') != token:
            raise Unauthorized('Invalid app token')
        permission = Permission.loads(app_name)
        _request_ctx_stack.top.current_identity = identity = User('', [permission])
    else:
        token = authorization_list[1]
        try:
            _request_ctx_stack.top.current_identity = identity = User.loads(_crypto.decrypt(token))
        except InvalidToken:
            raise Unauthorized('Invalid Token')
        if identity is None:
            raise Unauthorized('Token in request headers empty')
    if role not in identity.roles:
        raise Unauthorized('Token role not matched, get {}. expect {}'.format(identity.roles, role))


def token_required(role=Permission.USER):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _token_required(role)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_crypto_token(id_: str):
    return _crypto.encrypt(User(openid=id_).dumps())


if __name__ == '__main__':
    fer = Fernet(Fernet.generate_key())
    x = fer.encrypt(User(openid="test").dumps().encode())
    y = User.loads(fer.decrypt(x))
    print(x)
    print(y)
