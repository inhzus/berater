# -*- coding: utf-8 -*-
# created by inhzus

from datetime import datetime

from flask import current_app
from pytz import timezone

from berater.utils import current_identity
from berater.utils.wechat_sdk import send_template_msg, TemplateFormat


def send_register_msg(name: str):
    shanghai_timezone = timezone('Asia/Shanghai')
    time_str = datetime.now(shanghai_timezone).strftime('%m/%d/%Y %H:%M')
    data = TemplateFormat.register.format(touser=current_identity.openid, name=name, time=time_str)
    current_app.logger.info(send_template_msg(current_app.config['API_KEY'], current_app.config['API_SECRET'], data))
