# coding:utf-8

from tornado.options import define,options
import tornado.httpserver
import tornado.ioloop
from urls import handlers
import conf
import torndb
import redis

define('port',default=8500,type=int,help='run server on the given port')

class Application(tornado.web.Application):
    def __init__(self,*args,**kwargs):
        super(Application,self).__init__(*args,**kwargs)
        
        self.db = torndb.Connection(**conf.mysql_options)

        self.redis = redis.StrictRedis(**conf.redis_options)

def main():
    options.logging = conf.log_level
    options.log_file_prefix = conf.log_path
    tornado.options.parse_command_line()
    app = Application(
        handlers, **conf.settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()