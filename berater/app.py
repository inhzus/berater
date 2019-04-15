# -*- coding: utf-8 -*-
# created by inhzus

from flask import Flask

from berater.config import config
from berater.utils import Crypto


def create_app(config_name='dev'):
    app = Flask(__name__)

    # configure app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    config[0] = config[config_name]

    crypto = Crypto(app)
    crypto.init_app(app)

    from berater.chat import chat
    app.register_blueprint(chat)

    from berater.api import api
    app.register_blueprint(api)

    from berater.exception import error
    app.register_blueprint(error)

    return app
