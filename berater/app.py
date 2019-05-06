# -*- coding: utf-8 -*-
# created by inhzus

from flask import Flask

from berater.config import config
from berater.utils import Crypto
from berater.misc import engine


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

    from berater.chat import chat
    app.register_blueprint(chat, url_prefix='/chat')

    from berater.face import face
    app.register_blueprint(face, url_prefix='/api/face')

    from berater.api import api
    app.register_blueprint(api, url_prefix='/api')

    from berater.exception import error
    app.register_blueprint(error)

    return app
