# coding:utf-8

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os
import torndb
import config
import redis

from urls import urls
from tornado.options import options, define
from tornado.web import RequestHandler

from utils.redis_task_helper import RedisHelper

define("port", default=9200, type=int, help="run server on the given port")
define("debug", default='', type=str, help="")

class Application(tornado.web.Application):
    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        self.db = torndb.Connection(**config.mysql_options)
        self.redis = RedisHelper(**config.redis_options)

def main():
    tornado.options.parse_command_line()
    if options.debug != '':
        config.IS_DEBUG = True if options.debug == 'true' else False

    # 关闭日志文件
    if not config.IS_DEBUG:
        options.log_file_prefix = config.log_path
        options.logging = config.log_level
        # 日志按照时间分割
        options.log_rotate_mode = 'time'
        # 按照一天分割
        options.log_rotate_when = 'D'
        # 增量平率1
        options.log_rotate_interval = 1
    app = Application(
        urls,
        **config.settings
    )
    # xheaders=True 获取真实IP
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
