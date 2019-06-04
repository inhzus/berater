# -*- coding: utf-8 -*-
# created by inhzus

from enum import Enum
from functools import wraps
import json
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
    @staticmethod
    def loads(s: str) -> 'Permission':
        d = {
            'face': Permission.FACE,
            'user': Permission.USER
        }
        return d.get(s, Permission.EMPTY)


class User:
    def __init__(self, openid, role: Permission = Permission.USER):
        self.openid = openid
        self.role = role

    def dumps(self):
        return json.dumps({"openid": self.openid, "role": self.role.value})

    @staticmethod
    def loads(data):
        d = json.loads(data)
        u = User(openid=d["openid"], role=Permission(d["role"]))
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


def _token_required():
    authorization_list: List[str] = request.headers.get(current_app.config['CRYPTO_HEADER_KEY'], '').split(' ')
    if len(authorization_list) < 2:
        raise Unauthorized('Token not in request headers')
    if len(authorization_list) == 3:
        app_name = authorization_list[1]
        token = authorization_list[2]
        app_token: dict = current_app.config['APP_TOKEN']
        if app_token.get(app_name, '') != token:
            raise Unauthorized('Invalid app token')
        permission = Permission.loads(app_name)
        _request_ctx_stack.top.current_identity = User('', permission)
        return
    token = authorization_list[1]
    try:
        _request_ctx_stack.top.current_identity = identity = User.loads(_crypto.decrypt(token))
    except InvalidToken:
        raise Unauthorized('Invalid Token')
    if identity is None:
        raise Unauthorized('Token in request headers empty')


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        _token_required()
        return func(*args, **kwargs)

    return decorator


def get_crypto_token(id_: str):
    return _crypto.encrypt(User(openid=id_).dumps())


if __name__ == '__main__':
    fer = Fernet(Fernet.generate_key())
    x = fer.encrypt(User(openid="test").dumps().encode())
    y = User.loads(fer.decrypt(x))
    print(x)
    print(y)
