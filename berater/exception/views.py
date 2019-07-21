# -*- coding: utf-8 -*-
# created by inhzus

from traceback import extract_tb, StackSummary

from flask import Blueprint, jsonify, current_app, request
from werkzeug.exceptions import *

error = Blueprint('errors', __name__)


@error.app_errorhandler(HTTPException)
def handle_http_exceptions(err: HTTPException):
    current_app.logger.warning('code: {}, http exception: {}, Authorization: {}, Body: {}'.format(
        err.code, err.description, request.headers.get('Authorization', ''), request.json))
    return jsonify(code=err.code, error=err.description, data=None)


@error.app_errorhandler(Exception)
def handle_exceptions(err: Exception):
    msg = '\n'.join(['', ''.join(StackSummary.from_list(extract_tb(err.__traceback__)).format()), repr(err)])
    current_app.logger.error(msg)
    return jsonify(code=500, error=repr(err), data=None)
