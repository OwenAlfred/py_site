# coding:utf-8

import uuid
import json
import logging

from conf import SESSION_EXPIRES_SECONDS


class Session(object):
    """"""
    def __init__(self, request_handler_obj):

        # 先判断用户是否已经有了session_id
        self._request_handler = request_handler_obj
        # get_secure_cookie()返回的是bytes
        self.session_id = request_handler_obj.get_secure_cookie("session_id")
        print('从浏览器的cookie取出的session_id为%s' % self.session_id)

        # 如果不存在session_id,生成session_id
        if not self.session_id:
            self.session_id = uuid.uuid4().hex
            print('生成的session_id为%s' % self.session_id)
            self.data = {}
            request_handler_obj.set_secure_cookie("session_id", self.session_id)

        # 如果存在session_id, 去redis中取出data
        else:
            try:
                json_data = request_handler_obj.redis.get("sess_%s" % self.session_id.decode('utf-8'))
            except Exception as e:
                logging.error(e)
                # redis查询失败时，就当用户未登录
                self.data = {} 

            # redis中对应session_id没有查到session信息，说明session已经过期
            if not json_data:
                self.data = {}
            else:
                # 查询到redis中的session信息，将其反序列化成字典给Session对象的data属性
                self.data = json.loads(json_data)

    def save(self):
        # 将Session对象的data属性序列化为字符串
        json_data = json.dumps(self.data)
        try:
            # 将序列化后的session信息存到redis中
            self._request_handler.redis.setex("sess_%s" % self.session_id.decode('utf-8'),
                                             SESSION_EXPIRES_SECONDS, json_data)
        except Exception as e:
            logging.error(e)
            raise e

    def clear(self):
        # 删除浏览器中名为session_id的cookie，实为将其内容设置为空，删除cookie是由浏览器操作
        self._request_handler.clear_cookie("session_id")

        # 删除redis中保存的session信息
        try:
            self._request_handler.redis.delete("sess_%s" % self.session_id.decode('utf-8'))
        except Exception as e:
            logging.error(e)


"""
class xxxxhandler(RequestHandler):
    def post(self):

        session = Session(self)
        session.session_id
        session.data["username"] = "abc"
        session.data["mobile"] = "abc"
        session.save()

    def get(self):
        session = Session(self)
        session.data["username"] = "def"
        session.save()



    def get(self):
        session = Session(self)
        session.clear()

        session.clear()

redis中的数据：
key:    session_id
value:  data
"""
