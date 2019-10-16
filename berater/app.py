# -*- coding: utf-8 -*-
# created by inhzus

import logging
from json import JSONEncoder

from flask import Flask

from berater.config import config
from berater.misc import engine
from berater.utils import Crypto, get_file_log_handler


# noinspection SpellCheckingInspection
def create_app(config_name='dev'):
    # noinspection PyShadowingNames
    app = Flask(__name__)

    # configure app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    config[0] = config[config_name]

    handler = get_file_log_handler('log/berater.log')
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
