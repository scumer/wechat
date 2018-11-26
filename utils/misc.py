# encoding=utf-8

from wechatpy import WeChatClient

import setting


def wechat_client():
    return WeChatClient(setting.WechatConf['appid'], setting.WechatConf['secret'])