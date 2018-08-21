# coding:utf-8

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
import hashlib
import logging
import constants
import re
import conf
from utils.commons import required_login

class IndexHandler(BaseHandler):
    def get(self):
        logging.debug('debug msg')
        logging.info('info msg')
        logging.warning('warning msg')
        logging.error('error msg')
        print ('logging msg')
        self.write('website index page.')


class RegisterHandler(BaseHandler):
    def post(self):
        # 获取传入的参数
        mobile = self.json_dict['mobile']
        phonecode = self.json_dict['phonecode']
        password = self.json_dict['password']
        password2 = self.json_dict['password2']

        if not all((mobile, phonecode, password, password2)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='有未填的表单项'))

        if not re.match(r'^1[3578]\d{9}$', mobile):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='手机号格式错误'))

        # 校验传入的密码
        if password != password2:
            return self.write(dict(errcode=RET.DATAERR, errmsg='输入的两次密码不一致'))

        redis_phonecode = self.redis.get('%s%s' % (constants.SMS_CODE_REDIS_PREFIX, mobile))
        if not redis_phonecode:
            return self.write(dict(errcode=RET.NODATA, errmsg='短信验证码已过期'))

        # 验证短信验证码 
        # print(redis_phonecode)
        if phonecode != redis_phonecode:
            return self.write(dict(errcode=RET.DATAERR, errmsg='短信验证码填写错误'))

        # 密码加密
        pwd = hashlib.sha256((password + conf.PASSWD_HASH_KEY).encode('utf-8')).hexdigest()

        # 保持注册信息到数据库
        try:
            self.db.execute('insert into ih_user_profile(up_name, up_mobile, up_passwd) values(%(up_name)s, %(up_mobile)s, %(up_passwd)s)', \
                up_name=mobile, up_mobile=mobile, up_passwd=pwd)
        except Exception as e:
            logging.error(e)
            # 数据库中mobile字段设置了unique唯一约束,插入失败说明此手机号已经注册
            return self.write(dict(errcode=RET.DATAEXIST, errmsg='此手机号已注册，直接登录即可'))

        self.write(dict(errcode=RET.OK, errmsg='注册成功'))


class LoginHandler(BaseHandler):
    def post(self):
        # 获取传入的参数
        mobile = self.json_dict['mobile']
        password = self.json_dict['password']

        # 检验参数
        if not all((mobile,password)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='参数不完整'))

        try:
            res = self.db.get('select up_user_id, up_name, up_real_name, up_passwd,up_avatar, up_id_card from ih_user_profile where up_mobile=%s', mobile)
            # print('登录时查询到的结果：%s' % res)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库查询错误'))

        # 如果没查询到用户的信息记录
        if not res:
            return self.write(dict(errcode=RET.USERERR, errmsg='用户不存在或未激活'))
        # 如果输入的密码不正确
        if hashlib.sha256((password + conf.PASSWD_HASH_KEY).encode('utf-8')).hexdigest() != res['up_passwd']:
            return self.write(dict(errcode=RET.PWDERR, errmsg='密码错误'))

        # 登录成功，存入session
        self.session = Session(self) 
        self.session.data['user_id'] =  res['up_user_id']
        self.session.data['user_name'] = res['up_name']
        self.session.data['mobile'] = mobile
        self.session.data['avatar'] = conf.AVATAR_URL_PREFIX + res['up_avatar']
        self.session.data['real_name'] = res['up_real_name']
        self.session.data['id_card'] = res['up_id_card']
        print('登录成功时，conf.AVATAR_URL_PREFIX是 %s, res["up_avatar"]是 %s, self.session.data["avatar"]是 %s' % (conf.AVATAR_URL_PREFIX, res["up_avatar"], self.session.data['avatar']))
        self.session.save()

        self.write(dict(errcode=RET.OK, errmsg='登录成功'))


class CheckLoginHandler(BaseHandler):
    
    def get(self):
        # get_current_user方法在BaseHandler中已实现，它的返回值是session.data（用户保存在redis中
        # 的session数据），如果为{} ，意味着用户未登录;否则，代表用户已登录
        if not self.get_current_user():
            return self.write(dict(errcode=RET.SESSIONERR))
            
        self.write(dict(errcode=RET.OK, data=self.get_current_user()))


class LogoutHandler(BaseHandler):
    @required_login
    def get(self):
        # self.session = Session(self)
        self.session.clear()

        self.write(dict(errcode=RET.OK))