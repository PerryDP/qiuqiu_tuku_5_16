# -*- encoding: utf-8 -*-
"""
@File    : tools.py
@Time    : 2019/10/11 13:49
@Author  : Perry
@Email   : 3500396415@qq.com
@Software: PyCharm
"""
import datetime
import hashlib
import json
import random
import re
import string
from decimal import Decimal

import config


def get_random_str(char=0, num=0):
    '''
    获取随机数
    :param char: 字母位数
    :param num: 数字位数
    :return: 随机字符
    '''
    ran_str = ''
    if char:
        ran_str += ''.join(random.choices(string.ascii_letters, k=char))
    if num:
        ran_str += ''.join(random.choices(string.digits, k=num))
    return ran_str


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            # 添加decimal 数字类型转float
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


def object_to_str(obj):
    return json.dumps(obj, cls=DateEncoder)


def generate_password(password):
    '''
    生成加密密码
    :param password:
    :return:
    '''
    byte_pwd = (password + config.PASSWD_HASH_KEY).encode('utf-8')

    passwd = hashlib.sha256(byte_pwd).hexdigest()

    return passwd


def generate_UID():
    '''
    生成2位字母加6为数字的uid
    :return:
    '''
    uid = ''.join(random.choices(string.ascii_letters, k=2) + random.choices(string.digits, k=6))

    return uid
if __name__ == '__main__':
    salt = get_random_str(char=6)
    print(salt)
    print(generate_password('123456321' + salt))

