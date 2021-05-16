# coding:utf-8
import datetime
import os

STATIC_ROOT = '/static/'
# 是否debug模式
IS_DEBUG = True

# 项目根目录绝对路径
PROJECT_ROOT = os.path.dirname(__file__)

# Application配置参数
settings = dict(
    template_path='templates',
    # 有多个静态文件目录时删除static_path设置，在url中添加
    # static_path=os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret="FhLXI+BRRomtuaG47hoXEg3JCdi0BUi8vrpWmoxaoyI=",
    # 测试时关闭
    # xsrf_cookies=False if IS_DEBUG else True,
    # xsrf_cookies=True,
    debug=IS_DEBUG,
    # websocket 检测机制  心跳检测
    websocket_ping_interval=20,
    # 默认既是30秒钟没有收到ping 即关闭连接
    # websocket_ping_timeout=30
)

mysql_options = dict(
    host="localhost",
    database="tuku",
    password="123456321",
    user="root",
    # 时区设置
    time_zone='+8:00',
    charset='utf8mb4'
)

# Redis配置参数
# decode_responses 取出数据时自动解码，否则的话取出的都是二进制数据
redis_options = dict(
    host="localhost",
    port=6379,
    decode_responses=True
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 日志配置
log_path = os.path.join(os.path.dirname(__file__), "logs/log")
log_level = "debug"

# 密码加密密钥
PASSWD_HASH_KEY = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="

PIC_CODE_EXPIRES_SECONDS = 60 * 3  # 图片验证码的有效期，单位秒
SMS_CODE_EXPIRES_SECONDS = 60 * 15  # 短信验证码的有效期，单位秒

# ===========================jwt 配置 start=========================

# 后台jwt验证秘钥
JWT_ADMIN_SECRET_KEY = 'pqvKR8GE3DADma5D2yjZlyNs3N96Wx2W'
# 后台jwt过期时间
JWT_ADMIN_EXP_TIME = 60 * 12
# ===========================jwt 配置 end=========================

