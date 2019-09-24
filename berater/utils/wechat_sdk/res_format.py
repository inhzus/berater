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

    register = '''
    {{
        "touser": "{touser}",
        "template_id": "MxRIKUqWhANpXOAKdZp9d3_fv6WFOuOYaZGdKSLtCzU",
        "topcolor": "#FF0000",
        "data": {{
            "first": {{
                "value": "您好，报名操作成功。",
                "color": "#173177"
            }},
            "keyword1": {{
                "value": "NOVA 智能决策工作室",
                "color": "#173177"
            }},
            "keyword2": {{
                "value": "{name}",
                "color": "#173177"
            }},
            "keyword3": {{
                "value": "{time}",
                "color": "#173177"
            }},
            "remark": {{
                "value": "感谢您的参与。",
                "color": "#173177"
            }}
        }}
    }}
    '''
    '''format: touser, name, time'''

    unregister = '''
    {{
        "touser": "{touser}",
        "template_id": "YkO-jmcfMTFygvuM7DQ6AT4S5UH0XjkvLpxbz5i08Xc",
        "topcolor": "#FF0000",
        "data": {{
            "first": {{
                "value": "您好，取消报名操作成功。",
                "color": "#173177"
            }},
            "keyword1": {{
                "value": "NOVA 智能决策工作室",
                "color": "#173177"
            }},
            "keyword2": {{
                "value": "{name}",
                "color": "#173177"
            }},
            "keyword3": {{
                "value": "{time}",
                "color": "#173177"
            }},
            "remark": {{
                "value": "感谢您的参与。",
                "color": "#173177"
            }}
        }}
    }}
    '''
    '''format: touser, name, time'''
