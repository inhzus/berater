# -*- coding: utf-8 -*-
# created by inhzus

from traceback import extract_tb, StackSummary

from flask import Blueprint, jsonify, current_app, request
from werkzeug.exceptions import *

error = Blueprint('errors', __name__)


@error.app_errorhandler(HTTPException)
def handle_http_exceptions(err: HTTPException):
    current_app.logger.warning('code: {}, http exception: {}'.format(err.code, err.description))
    return jsonify(code=err.code, error=err.description, data=None), 200


@error.app_errorhandler(Exception)
def handle_exceptions(err: Exception):
    msg = '\n'.join(['', ''.join(StackSummary.from_list(extract_tb(err.__traceback__)).format()), repr(err)])
    current_app.logger.error(msg)
    return jsonify(code=500, error=repr(err), data=None), 200


@error.after_app_request
def after_request(response: 'Response'):
    current_app.logger.info('{} {} "{}" Auth: "{}" "{}"'.format(
        request.method, request.full_path, request.headers.get('User-Agent'),
        request.headers.get('Authorization', ''), request.json if request.json else ''))
    current_app.logger.info('{} Return: {}'.format(response.status, response.data.decode('utf-8')))
    return response
