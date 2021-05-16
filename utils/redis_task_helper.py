# -*- encoding: utf-8 -*-
"""
@File    : redis_task_helper.py
@Time    : 2019/10/11 14:01
@Author  : Perry
@Email   : 3500396415@qq.com
@Software: PyCharm
"""
import json

from redis import StrictRedis

import config


class RedisHelper(StrictRedis):
    '''
    一般redis存储位置
    '''
    # 短信验证码
    key_ver_code = 'vercode:{region}:{phone}'
    key_ver_code_time = 60 * 5
    # uuid4 校验 短信验证码
    key_verification_token = 'token:{v_type}'
    # 用户缓存信息 8位随机字符串
    key_user_cache = 'user:cache:{ran_str}'
    # Admin登录验证码 序号
    key_verify_code = 'verify:login:{vernum}:{ip}'
    # 普通用户登录验证码
    key_verify_code_user = 'verify:login:{username}:{code}'
    # 密码错误次数
    key_pwd_err_num = 'pwd:err:{username}'
    # 路由信息表
    key_route_view = 'router:view:{role_id}'
    # api路由信息表
    key_route_api = 'router:api:{role_id}'

    def set_router_view(self, role_id, value):
        if isinstance(value, list):
            value = json.dumps(value)
        key = self.key_route_view.format(role_id=role_id)

        self.set(key, value)

    def get_router_view(self, role_id):
        rotuer = self.get(self.key_route_view.format(role_id=role_id))
        try:
            return json.loads(rotuer)
        except Exception as e:
            return ''

    def set_router_api(self, role_id, value):
        if isinstance(value, list):
            value = json.dumps(value)
        key = self.key_route_api.format(role_id=role_id)

        self.set(key, value)

    def get_router_api(self, role_id):
        rotuer = self.get(self.key_route_api.format(role_id=role_id))
        try:
            return json.loads(rotuer)
        except Exception as e:
            return ''

    def __init__(self, *args, **kwargs):
        # db 0 custormer_server 旧版 1 weibar 新版
        super().__init__(db=1, *args, **kwargs)

    def set_verify_code(self, vernum, ip, code):
        '''
        设置验证码,
        :param code: 验证码内容
        :param member_id: 用户id
        :param ip: 用户ip
        :return:
        '''
        redis_verify_code = self.key_verify_code.format(vernum=vernum, ip=ip)
        self.setex(redis_verify_code, config.PIC_CODE_EXPIRES_SECONDS, code)

    def get_verify_code(self, vernum, ip):
        '''
        获取验证码
        :param vernum:
        :param ip:
        :return:
        '''
        redis_verify_code = self.key_verify_code.format(vernum=vernum, ip=ip)
        ver_code = self.get(redis_verify_code)
        return ver_code if ver_code else None

    def set_user_verify_code(self, username, code):
        key = self.key_verify_code_user.format(username=username, code=code)
        ex = 60 * 5
        self.set(key, 1, ex=ex)

    def get_user_verify_code(self, username, code):
        key = self.key_verify_code_user.format(username=username, code=code)
        val = self.get(key)
        return val

    def delete_verify_code(self, random_num, ip):
        '''
        删除用户验证码
        :param member_id:
        :param ip:
        :return:
        '''
        redis_verify_code = self.key_verify_code.format(memberID=random_num, ip=ip)
        self.delete(redis_verify_code)

    def set_pwd_error_time(self, username, times):
        '''
        用户名，次数
        :param username:
        :param times:
        :return:
        '''
        key = self.key_pwd_err_num.format(username=username)
        ex = 60 * 5
        self.set(key, times, ex)

    def get_pwd_error_times(self, username):
        key = self.key_pwd_err_num.format(username=username)
        return self.get(key)
