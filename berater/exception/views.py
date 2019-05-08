# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint, jsonify
from werkzeug.exceptions import *

error = Blueprint('errors', __name__)


@error.app_errorhandler(HTTPException)
def handle_http_exceptions(err: HTTPException):
    return jsonify(code=err.code, error=err.description, data=None)
