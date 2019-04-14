# -*- coding: utf-8 -*-
# created by inhzus

from dataclasses import dataclass


@dataclass()
class Response:
    data: dict
    code: int = 200
    error: str = 200
