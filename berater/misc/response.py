# -*- coding: utf-8 -*-
# created by inhzus

from flask import jsonify


class Response:
    def __init__(self, code: int = 200, error: str = '', **kwargs):
        self.code = code
        self.error = error
        self.data = kwargs if kwargs else None

    def json(self):
        return jsonify(code=self.code, error=self.error, data=self.data)
