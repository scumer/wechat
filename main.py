# coding=utf-8

import logging
import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.web

import setting
from handlers import *

Hanlders = [
    (r"/", WechatMsgHandler),
    (r"/index", IndexHandler),
]

class Application(tornado.web.Application):
    def __init__(self):
        self.init_logger()
        app_settings = dict(debug=True)
        tornado.web.Application.__init__(self, Hanlders, **app_settings)

    def init_logger(self):
        log_dir = './log'
        log_name = 'main.log'
        os.makedirs(log_dir, exist_ok=True)

        from logging.handlers import RotatingFileHandler
        logfile = RotatingFileHandler(os.path.join(log_dir, log_name), maxBytes=1024*1024*50, backupCount=10)

        formatter = logging.Formatter('[%(asctime)s %(process)d %(module)s:%(funcName)s:%(lineno)d %(levelname)5s] %(message)s', '%Y%m%d %H:%M:%S')
        logfile.setFormatter(formatter)
        logging.getLogger('').setLevel(logging.DEBUG)
        logging.getLogger('').addHandler(logfile)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s-%(process)5d-%(levelname)5s] %(message)s', '%H:%M:%S')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def start(self):
        http_server = tornado.httpserver.HTTPServer(self)
        http_server.listen(setting.Listen)

        logging.info(u'starting application... [%s]', str(os.getpid()))
        tornado.ioloop.IOLoop.instance().start()

    def stop(self):
        tornado.ioloop.IOLoop.instance().stop()


if __name__ == "__main__":
    try:
        app = Application()
        app.start()

    except KeyboardInterrupt as e:
        logging.info('stoping application...')
        app.stop()
    except Exception as e:
        logging.exception(e)
