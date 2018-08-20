# coding:utf-8

import json

from tornado.web import RequestHandler
from utils.session import Session

class BaseHandler(RequestHandler):
    '''hander基类'''
    @property
    def db(self):
        # 作为RequestHandler对象的db属性
        return self.application.db

    @property
    def redis(self):
        # 作为RequestHandler对象的redis属性
        return self.application.redis

    def get_current_user(self):
        # 判断用户是否登录
        self.session = Session(self)
        print('get_current_user()中，return的self.session.data为 %s' % self.session.data)
        return self.session.data

        # session_id = self.get_secure_cookie('session_id')
        # print('get_current_user()中的session_id是%s' % session_id)
        # if not session_id:
        #     return False

        # res = self.redis.get('session_id_%s' % session_id)
        # if not res:
        #     print('return了False')
        #     return False

        # print('get_current_user()中查询redis,res为%s' % res)
        # result = json.loads(res)
        # print('get_current_user()中查询redis中保存的session的username是%s' % result['user_name'])
        # return result

    def set_default_headers(self):
        # 设置默认的响应header
        self.set_header('Content-Type', 'applicationi/json; charset=UTF-8')

    def initialize(self):
        pass

    def prepare(self):
        '''预解析json数据'''
        # 设置_xsrf的Cookie值，可以在任意的Handler中通过获取self.xsrf_token的值来生成_xsrf并设置Cookie
        self.xsrf_token
        # print('自动设置了_xsrf的cookie')
        
        # 不能写成self.request.headers['Content-Type']
        # get('Content-Type','')是request没有Content-Type时返回‘’，
        # 这样再调用startswith()才不会报错：None type has no attribute startswith
        if self.request.headers.get('Content-Type','').startswith('application/json'):
            self.json_dict = json.loads(self.request.body)
        else:
            self.json_dict = {}

    def write_error(self, status_code, **kwargs):
        pass

    def on_finish(self):
        pass