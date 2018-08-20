# coding:utf-8

IMAGE_CODE_EXPIRE = 180 # 图片验证码的有效期，单位秒
SMSCODE_EXPIRE = 300 # 短信验证码的有效期，单位秒

IMAGE_CODE_REDIS_PREFIX = "image_code_"  # redis中保存的图片验证码key的前缀
SMS_CODE_REDIS_PREFIX = "sms_code_"  # redis中保存的短信验证码key的前缀

QINIU_URL_PREFIX = "http://o91qujnqh.bkt.clouddn.com/" # 七牛存储空间的域名

REDIS_AREA_INFO_EXPIRES_SECONDES = 86400 # redis缓存城区信息的有效期
REDIS_HOUSE_INFO_EXPIRES_SECONDES = 86400 # redis缓存房屋信息的有效期

HOME_PAGE_MAX_HOUSES = 5 # 主页房屋展示最大数量
HOME_PAGE_DATA_REDIS_EXPIRE_SECOND = 7200 # 主页缓存数据过期时间 秒

HOUSE_LIST_PAGE_CAPACITY = 3 # 房源列表页每页显示房屋数目
HOUSE_LIST_PAGE_CACHE_NUM = 2 # 房源列表页每次缓存页面书

REDIS_HOUSE_LIST_EXPIRES_SECONDS = 7200 # 列表页数据缓存时间 秒
