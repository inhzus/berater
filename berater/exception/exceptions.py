# -*- coding: utf-8 -*-
# created by inhzus


class BeraterException(Exception):
    pass


class BadRequestException(BeraterException):
    """400 Bad Request"""
    pass


class UnauthorizedException(BeraterException):
    """401 Unauthorized"""
    pass


class ForbiddenException(BeraterException):
    """403 Forbidden"""
    pass


class NotFoundException(BeraterException):
    """404 Not Found"""
    pass


class InternalServerException(BeraterException):
    """500 Internal Server Error"""
