# -*- coding: utf-8 -*-
# created by inhzus

import logging
import os
from json import JSONEncoder
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

from berater.config import config
from berater.misc import engine
from berater.utils import Crypto


def create_app(config_name='dev'):
    app = Flask(__name__)

    # configure app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    config[0] = config[config_name]

    crypto = Crypto(app)
    crypto.init_app(app)

    engine.init_app(app)
    engine.create_all(app=app)

    if not os.path.exists('log'):
        os.mkdir('log')
    handler = TimedRotatingFileHandler(
        'log/berater.log', delay=False, encoding='utf-8', interval=1, utc=True, when='D')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    logging.getLogger('werkzeug').addHandler(handler)
    logging.getLogger('sqlalchemy').addHandler(handler)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)

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

    from berater.api import api
    app.register_blueprint(api, url_prefix='/api')

    from berater.exception import error
    app.register_blueprint(error)

    return app


app = create_app('pro')
