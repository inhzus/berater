# -*- coding: utf-8 -*-
"""
Created by suun on 5/14/2018
"""


class MsgFormat(object):
    """
    post 给API 的所有xml 格式
    """

    text = "<xml>" \
           "<ToUserName><![CDATA[%s]]></ToUserName>" \
           "<FromUserName><![CDATA[%s]]></FromUserName>" \
           "<CreateTime>%s</CreateTime>" \
           "<MsgType><![CDATA[text]]></MsgType>" \
           "<Content><![CDATA[%s]]></Content>" \
           "</xml>"

    image = "<xml>" \
            "<ToUserName><![CDATA[%s]]></ToUserName>" \
            "<FromUserName><![CDATA[%s]]></FromUserName>" \
            "<CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[image]]></MsgType>" \
            "<Image>" \
            "<MediaId><![CDATA[%s]]></MediaId>" \
            "</Image>" \
            "</xml>"

    voice = "<xml>" \
            "<ToUserName><![CDATA[%s]]></ToUserName>" \
            "<FromUserName><![CDATA[%s]]></FromUserName>" \
            "<CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[voice]]></MsgType>" \
            "<Voice>" \
            "<MediaId><![CDATA[%s]]></MediaId>" \
            "</Voice>" \
            "</xml>"

    video = "<xml>" \
            "<ToUserName><![CDATA[%s]]></ToUserName>" \
            "<FromUserName><![CDATA[%s]]></FromUserName>" \
            "<CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[video]]></MsgType>" \
            "<Video>" \
            "<MediaId><![CDATA[%s]]></MediaId>" \
            "<Title><![CDATA[%s]]></Title>" \
            "<Description><![CDATA[%s]]></Description>" \
            "</Video> " \
            "</xml>"

    music = "<xml>" \
            "<ToUserName><![CDATA[%s]]></ToUserName>" \
            "<FromUserName><![CDATA[%s]]></FromUserName>" \
            "<CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[music]]></MsgType>" \
            "<Music>" \
            "<Title><![CDATA[%s]]></Title>" \
            "<Description><![CDATA[%s]]></Description>" \
            "<MusicUrl><![CDATA[%s]]></MusicUrl>" \
            "<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>" \
            "<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>" \
            "</Music>" \
            "</xml>"

    news_front = "<xml>" \
                 "<ToUserName><![CDATA[%s]]></ToUserName>" \
                 "<FromUserName><![CDATA[%s]]></FromUserName>" \
                 "<CreateTime>%s</CreateTime>" \
                 "<MsgType><![CDATA[news]]></MsgType>" \
                 "<ArticleCount>%d</ArticleCount>" \
                 "<Articles>"

    news_middle = "<item>" \
                  "<Title><![CDATA[%s]]></Title>" \
                  "<Description><![CDATA[%s]]></Description>" \
                  "<PicUrl><![CDATA[%s]]></PicUrl>" \
                  "<Url><![CDATA[%s]]></Url>" \
                  "</item>"

    news_back = "</Articles></xml>"


class TemplateFormat(object):
    """
    模板消息的格式化数据，必须按照严格json 格式和format 格式化要求
    """
    bind = '''
    {{
        "touser": "{touser}",
        "template_id": "4NjKBy5S6e5QzpymZHBMJTiJXAtnvo6dtlOGD-Lo97A",
        "topcolor": "#FF0000",
        "data": {{
            "first": {{
                "value": "您已成功绑定。",
                "color": "#173177"
            }},
            "keyword1": {{
                "value": "{account}",
                "color": "#173177"
            }},
            "keyword2": {{
                "value": "{time}",
                "color": "#173177"
            }},
            "remark": {{
                "value": "绑定成功，您可进行下一步操作。",
                "color": "#173177"
            }}
        }}
    }}
    '''

