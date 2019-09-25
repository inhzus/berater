# -*- coding: utf-8 -*-
# created by inhzus

import logging
import os
import sys
from json import JSONEncoder
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

from berater.config import config
from berater.misc import engine
from berater.utils import Crypto


# noinspection SpellCheckingInspection
def create_app(config_name='dev'):
    # noinspection PyShadowingNames
    app = Flask(__name__)

    # configure app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    config[0] = config[config_name]

    if not os.path.exists('log'):
        os.mkdir('log')

    class PackagePathFilter(logging.Filter):
        def filter(self, record):
            pathname = record.pathname
            record.relative_path = None
            abs_sys_paths = map(os.path.abspath, sys.path)
            # noinspection PyTypeChecker
            for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
                if not path.endswith(os.sep):
                    path += os.sep
                if pathname.startswith(path):
                    record.relative_path = os.path.relpath(pathname, path)
                    break
            if record.relative_path.endswith('.py'):
                record.relative_path = record.relative_path[:-3]
            record.relative_path = record.relative_path.replace('/', '.')
            return True

    handler = TimedRotatingFileHandler(
        'log/berater.log', delay=False, encoding='utf-8', interval=1, utc=True, when='D')
    handler.addFilter(PackagePathFilter())
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter('[%(asctime)s] %(levelname)s %(relative_path)s:%(lineno)s %(message)s'))
    # logging.getLogger('gunicorn.error').addHandler(handler)
    # logging.getLogger('werkzeug').addHandler(handler)
    logging.getLogger('sqlalchemy').addHandler(handler)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

    crypto = Crypto(app)
    crypto.init_app(app)

    engine.init_app(app)
    engine.create_all(app=app)

    # Json encoder set ensure ASCII false
    class NonASCIIEncoder(JSONEncoder):
        def __init__(self, **kwargs):
            kwargs['ensure_ascii'] = False
            super(NonASCIIEncoder, self).__init__(**kwargs)

    app.json_encoder = NonASCIIEncoder

    from berater.chat import chat
    app.register_blueprint(chat, url_prefix='/chat')

    from berater.face import face
    app.register_blueprint(face, url_prefix='/api/face')

    from berater.admin import admin
    app.register_blueprint(admin, url_prefix='/api/admin')

    from berater.nova import nova
    app.register_blueprint(nova, url_prefix='/api/nova')

    from berater.api import api
    app.register_blueprint(api, url_prefix='/api')

    from berater.exception import error
    app.register_blueprint(error)

    return app


app = create_app('pro')
