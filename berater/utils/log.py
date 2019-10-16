# -*- coding: utf-8 -*-
# created by inhzus

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler


class PackagePathFilter(logging.Filter):
    def filter(self, record):
        pathname = record.pathname
        record.relative_path = None
        abs_sys_paths = map(os.path.abspath, sys.path)
        # noinspection PyTypeChecker
        for path in sorted(abs_sys_paths, key=len, reverse=True):  # longer paths first
            if not path.endswith(os.sep):
                path += os.sep
            if pathname.startswith(path):
                record.relative_path = os.path.relpath(pathname, path)
                break
        if record.relative_path.endswith('.py'):
            record.relative_path = record.relative_path[:-3]
        record.relative_path = record.relative_path.replace('/', '.')
        return True


def get_file_log_handler(filename):
    handler = TimedRotatingFileHandler(
        filename, delay=False, encoding='utf-8', interval=1, utc=True, when='D', backupCount=30)
    handler.addFilter(PackagePathFilter())
    handler.setLevel(logging.DEBUG)
    # noinspection SpellCheckingInspection
    handler.setFormatter(
        logging.Formatter('[%(asctime)s] %(levelname)s %(relative_path)s:%(lineno)s %(message)s'))
    return handler
