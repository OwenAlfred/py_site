#coding:utf-8

from .BaseHandler import BaseHandler
from utils.response_code import RET
import logging
import conf
import uuid
from utils.commons import required_login


class ProfileHandler(BaseHandler):
    @required_login
    def get(self):
        self.write(dict(errcode=RET.OK, data=self.session.data))


class AvatarHandler(BaseHandler):
    @required_login
    def post(self):
        if not self.request.files['avatar']:
            return None

        # 获取用户上传的头像的二进制数据和原文件名
        avatar_up_loaded = self.request.files['avatar'][0]['body']
        avatar_oriname = self.request.files['avatar'][0]['filename']
        
        # 获取头像的扩展名
        try:
            name_suffix = avatar_oriname[avatar_oriname.rindex('.') : ]
        except Exception as e:
            logging.error(e)
            name_suffix = '.jpg'

        # 为上传的头像生成唯一的名字
        avatar_rename = uuid.uuid4().hex

        # 保存上传的头像到服务器
        try:
            with open('%s%s%s' % (conf.AVATAR_URL_PREFIX, avatar_rename, name_suffix), 'wb') as w:
                w.write(avatar_up_loaded)
        except Exception as e:
            logging.error(e)
            return None


        # 保存头像地址到数据库的用户表
        try:
            self.db.execute('update ih_user_profile set up_avatar=%(avatar)s where up_mobile=%(mobile)s', avatar=avatar_rename+name_suffix, mobile=self.session.data['mobile'])
        except Exception as e:
            logging.error(e)
            print('avatar保存到数据库失败')
            return None

        else:
            # 更新session中的头像信息 
            self.session.data['avatar'] = conf.AVATAR_URL_PREFIX + avatar_rename + name_suffix
            # session的data属性更改后需要保存，redis中的信息才会更新
            self.session.save()
            # 返回头像保存路径
            self.write(dict(errcode=RET.OK, data='%s%s%s' % (conf.AVATAR_URL_PREFIX, avatar_rename, name_suffix))) 



class NameHandler(BaseHandler):
    @required_login
    def post(self):
        # 获取传入的用户名
        name = self.json_dict['name'].strip()
        # 如果用户名为空
        if not name:
            return self.write(dict(errcode=RET.PARAMERR))

        # # 查询数据库用户名是否已存在
        # try:
        #     res = self.db.get('select * from ih_user_profile where up_name=%s', name)
        # except Exception as e:
        #     logging.error(e)
        #     return self.write(dict(errcode=RET.DBERR))

        # # 用户名已存在
        # if res:
        #     return self.write(dict(errcode=RET.DATAEXIST))

        #更新数据库
        try:
            result = self.db.execute('update ih_user_profile set up_name=%(name)s where up_mobile=%(mobile)s', name=name, mobile=self.session.data['mobile'])
        except Exception as e:
            logging.error(e)
            # 数据库字段up_name设置了unique唯一约束，更新失败说明传入的用户名已存在
            return self.write(dict(errcode=RET.DBERR, errmsg='此用户名已存在'))
        else:
            # 更新session中的name
            self.session.data['user_name'] = name
            # 将更新后的session保存到redis中
            self.session.save()
            return self.write(dict(errcode=RET.OK))



class AuthHandler(BaseHandler):
    @required_login
    def get(self):
        return self.write(dict(errcode=RET.OK, data=self.session.data))


    @required_login
    def post(self):
        # 获取真名和身份证号
        real_name = self.json_dict['real_name'].strip()
        id_card = self.json_dict['id_card'].strip()

        # 检验参数
        if not all((real_name, id_card)):
            return self.write(dict(errcode=RET.PARAMERR,errmsg='参数不完整'))

        # 查询数据库是否有相同身份证号
        try:
            res = self.db.get('select * from ih_user_profile where up_id_card=%s', id_card)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.ROLEERR,errmsg='用户身份错误，已有相同身份证号'))

        # 数据库已有相同身份证号
        if res:
            return self.write(dict(errcode=RET.ROLEERR,errmsg='用户身份错误，已有相同身份证号'))

        # 将真名和证件号存入数据库
        try:
            self.db.execute('update ih_user_profile set up_real_name=%(real_name)s, up_id_card=%(id_card)s', real_name=real_name, id_card=id_card)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.ROLEERR,errmsg='用户身份错误，已有相同身份证号'))

        # 将真名和证件号存入session
        # self.session = Session(self)  # BaseHandler的get_current_user()中已经新建了Session赋值给self.session
        self.session.data['real_name'] = real_name
        self.session.data['id_card'] = id_card
        # 将更新后的data存入redis
        self.session.save()

        return self.write(dict(errcode=RET.OK))