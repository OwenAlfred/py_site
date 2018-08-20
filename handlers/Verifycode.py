# coding:utf-8

from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha
from libs.yuntongxun.CCP import ccp
from utils.response_code import RET
import random
import re
import constants
import conf
import logging


class ImagecodeHandler(BaseHandler):
    def get(self):
        pre = self.get_argument('pre', '')
        cur = self.get_argument('cur')

        if pre:
            try:
                self.redis.delete('%s%s' %
                                  (constants.IMAGE_CODE_REDIS_PREFIX, pre))
            except Exception as e:
                logging.error(e)

        # name 图片验证码名称   text 图片验证码文本   image 图片验证码二进制数据
        name, text, image = captcha.generate_captcha()

        try:
            # self.redis.setex(name, expries, value)
            self.redis.setex('%s%s' % (
                constants.IMAGE_CODE_REDIS_PREFIX, cur), constants.IMAGE_CODE_EXPIRE, text)
        except Exception as e:
            logging.error(e)

        self.set_header('Content-Type', 'image/jpeg')
        return self.write(image)


class SMScodeHandler(BaseHandler):
    def post(self):
        print('json_dict为%s' % self.json_dict)
        # 获取参数
        mobile = self.json_dict['mobile']
        piccode = self.json_dict['piccode']
        piccode_id = self.json_dict['piccode_id']

        # 参数校验
        # if mobile and piccode and piccode_id
        if not all((mobile, piccode, piccode_id)):
            return self.write(dict(errcode=RET.DATAERR, errmsg='有未填的表单项'))
        
        # 判断手机号
        if not re.match(r'^1[3578][0-9]{9}$', mobile):
            return self.write(dict(errcode=RET.PARAMERR, errmsg='手机号格式不正确'))

        # 查询手机号是否已经注册

        isregisted = self.db.get('select * from ih_user_profile where up_mobile=%s', mobile)
        # print(isregisted)
        if isregisted:
            return self.write(dict(errcode=RET.DATAEXIST, errmsg='此手机号已注册，直接登录即可'))
            


        # 查询redis中的图片验证码
        try:
            redis_piccode = self.redis.get('%s%s' % (constants.IMAGE_CODE_REDIS_PREFIX, piccode_id))
            print('redis_piccode为%s, piccode为%s, piccode.upper()为%s' % (redis_piccode, piccode, piccode.upper()))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库查询出错！'))
        
        # 判断图片验证码

        if not redis_piccode:
            return self.write(dict(errcode=RET.NODATA, errmsg='图片验证码已过期'))
        
        if redis_piccode != piccode.upper():
            return self.write(dict(errcode=RET.DATAERR, errmsg='输入的图片验证码错误'))
        
        # 输入的图片验证码正确
        # 产生随机短信验证码
        sms_code = random.randint(1, 999999)
        sms_code = '%06d' % sms_code
        print('code为%s' % sms_code)

        # 保存生成的短信验证码
        try:
            self.redis.setex('%s%s' % (constants.SMS_CODE_REDIS_PREFIX, mobile), constants.SMSCODE_EXPIRE, sms_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.DBERR, errmsg='数据库出错'))

        # 发送短信验证码
        try:
            result = ccp.sendTemplateSMS(mobile, [sms_code, int(constants.SMSCODE_EXPIRE / 60)], 1) # 返回True或False
        except Exception as e:
            logging.error(e)
            # 短信发送失败就需要把redis中已保存的短信验证码删除
            self.redis.delete('%s%s' % (constants.SMS_CODE_REDIS_PREFIX, mobile))
            return self.write(dict(errcode=RET.THIRDERR, errmsg='短信发送失败'))

        if not result:
            # 短信发送失败就需要把redis中已保存的短信验证码删除
            self.redis.delete('%s%s' % (constants.SMS_CODE_REDIS_PREFIX, mobile))
            return self.write(dict(errcode=RET.THIRDERR, errmsg='短信验证码发送失败'))
        
        self.write(dict(errcode=RET.OK, errmsg='短信验证码已发送，请查收'))