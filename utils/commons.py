#coding:utf-8

from utils.response_code import RET
import functools

# 验证用户登录装饰器
def required_login(func):
    @functools.wraps(func) # 保证被装饰的函数对象的__name__不变
    def wrapper(request_handler_obj, *args, **kwargs): 
        # 根据get_current_user()方法判断，如果返回的是空字典，说明用户没登录
        if not request_handler_obj.get_current_user():
            return request_handler_obj.write(dict(errcode=RET.SESSIONERR))

        # 如果get_current_user()方法返回的不是空字典，说明用户已登录
        func(request_handler_obj, *args, **kwargs)
    return wrapper