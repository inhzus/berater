# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint, jsonify
from .exceptions import *


EXCEPTION_STATUS_DICT = {
    BadRequestException: 400,
    UnauthorizedException: 401,
    ForbiddenException: 403,
    NotFoundException: 404,
    InternalServerException: 500
}


error = Blueprint('errors', __name__)


@error.app_errorhandler(BeraterException)
def handle_exceptions(err):
    return jsonify(code=EXCEPTION_STATUS_DICT[err.__class__], error=str(err))
