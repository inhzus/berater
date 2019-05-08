# -*- coding: utf-8 -*-
# created by inhzus

from functools import wraps

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


class Crypto:
    def __init__(self, app=None):
        # noinspection PyTypeChecker
        self.fer: Fernet = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        for k, v in CONFIG_DEFAULTS.items():
            app.config.setdefault(k, v)
        self.fer = Fernet(app.config['CRYPTO_KEY'])
        app.extensions['crypto'] = self

    def encrypt(self, data: str):
        return self.fer.encrypt(data.encode()).decode()

    def decrypt(self, data: str):
        return self.fer.decrypt(data.encode(), current_app.config['CRYPTO_TTL'])


_crypto = LocalProxy(lambda: current_app.extensions['crypto'])
current_identity = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_identity', None))


def _token_required():
    token = request.headers.get(current_app.config['CRYPTO_HEADER_KEY'], None).split(' ')[1]
    if token is None:
        raise Unauthorized('Token not in request headers')
    try:
        _request_ctx_stack.top.current_identity = identity = _crypto.decrypt(token).decode()
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
    return 'Bearer {}'.format(_crypto.encrypt(id_))
