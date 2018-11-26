# encoding=utf-8
import sys


# WebServer
Listen = 9090

# Wechat
WechatConf = {
    'appid': 'wxc3c362443aa96995',
    'secret': 'b9a8da8fe28787759a9fecd2c9e19bb1',
    'token': 'SFV'
}


get = lambda key, default = dict(): sys.modules[__name__].__dict__.get(key, default)