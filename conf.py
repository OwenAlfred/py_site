# coding:utf-8

import os

# Application配置参数
settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="FhLXI+BRRomtuaG47hoXEg3JCdi0BUi8vrpWmoxaoyI=",
        xsrf_cookies=True,
        debug=True
    )


# 数据库配置参数
mysql_options = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="root"
)

# Redis配置参数
redis_options = dict(
    host="127.0.0.1",
    port=6379,
    decode_responses=True   # 这样，在python3中，从redis取出的数据就是str类型的，如果设置为False(默认是False)，redis取出的是bytes类型
)

# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"

SESSION_EXPIRES_SECONDS = 86400 # session数据有效期， 单位秒

# 用户头像url前缀
AVATAR_URL_PREFIX = "./static/upload/avatar/"

# 上传的房屋图片url前缀
HOUSE_IMG_URL_PREFIX = "./static/upload/house/"

# 密码加密用的混淆密钥
PASSWD_HASH_KEY = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="