# coding=utf-8

import logging

import tornado.web
from wechatpy.utils import check_signature
# from wechatpy import WeChatClient
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import create_reply
from utils import msgdispatch, register_message, DEFAULT_MSG_HANDLER

import setting
from utils import wechat_client


_MY_OPENID = 'oz1ZK1KdUY-QTPJirfaI_lZhAQic'

# ============================================================================#
# Register Wechat Msg Handers
# ============================================================================#
@register_message('event.click.BTN_A')
def _(msg):
    reply = create_reply("BTN_A", message=msg)
    return reply.render()


@register_message('event.click.BTN_B')
def _(msg):
    reply = create_reply("BTN_B", message=msg)
    return reply.render()


@register_message('text')
def _(msg):
    reply = create_reply("^_^ %s" % msg.content, message=msg)
    return reply.render()


@register_message(DEFAULT_MSG_HANDLER)
def _(msg):
    reply = create_reply("welcome", message=msg)
    return reply.render()


@register_message('event.subscribe')
def _(msg):
    openid = msg.source
    client = wechat_client()
    user = client.user.get(openid)
    logging.debug(user)

    # 有人关注公众号后通知我:oz1ZK1KdUY-QTPJirfaI_lZhAQic
    res = client.message.send_text(_MY_OPENID, '%s 关注公众号' % user['nickname'])
    logging.debug(res)

    headimgurl = user['headimgurl']
    size_index = headimgurl.rfind('/')
    size_index = len(headimgurl) if size_index==-1 else size_index
    headimgurl = headimgurl[0:size_index]
    reply_msg = [{
        'title': '欢迎%s' % user['nickname'],
        'description': '',
        'image': headimgurl+'/0',
        'url':headimgurl+'/0'
    }]
    reply = create_reply(reply_msg, message=msg)
    return reply.render()


@register_message('event.unsubscribe')
def _(msg):
    openid = msg.source
    client = wechat_client()
    res = client.message.send_text(_MY_OPENID, '%s 取消关注公众号' % openid)
    logging.debug(res)
    return None
# ============================================================================ #
# ============================================================================ #


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write('Hello World!')


class WechatMsgHandler(tornado.web.RequestHandler):
    def get(self):
        signature = self.get_query_argument('signature')
        timestamp = self.get_query_argument('timestamp')
        nonce = self.get_query_argument('nonce')
        echostr = self.get_query_argument('echostr')
        token = setting.WechatConf['token']

        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException as e:
            logging.error(str(e))
            return self.send_error(403, str(e))
        else:
            return self.write(echostr)

    def post(self):
        msg = parse_message(self.request.body)
        logging.debug(msg)

        reply = msgdispatch(msg) or ''
        return self.write(reply)
