# -*- coding: utf-8 -*-
# created by inhzus

from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/info')
def update_info():
    pass


@api.route('/ems')
def ems_logistics():
    pass
