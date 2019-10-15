# -*- coding: utf-8 -*-
# created by inhzus

from datetime import datetime

from flask import current_app
from pytz import timezone

from berater.utils import current_identity, send_template_msg
from berater.utils.wechat_sdk import TemplateFormat


def _send_register_template_msg(name: str, fmt: str):
    shanghai_timezone = timezone('Asia/Shanghai')
    time_str = datetime.now(shanghai_timezone).strftime('%m/%d/%Y %H:%M')
    ret = send_template_msg(fmt.format(touser=current_identity.openid, name=name, time=time_str))
    current_app.logger.info('[template msg] send to {}, return {}'.format(name, ret))


def send_register_msg(name: str):
    _send_register_template_msg(name, TemplateFormat.register)


def send_unregister_msg(name: str):
    _send_register_template_msg(name, TemplateFormat.unregister)
