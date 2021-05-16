# -*- encoding: utf-8 -*-
"""
@File    : basehandler.py
@Time    : 2020/8/31 22:00
@Author  : Perry
@Email   : 3500396415@qq.com
@Software: PyCharm
"""
import copy
import json
import logging
import os
import random

import re
import socket
import time
import traceback
import urllib
import uuid
from decimal import Decimal

import jwt
from jwt import ExpiredSignatureError, DecodeError
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler, StaticFileHandler
from tornado.websocket import WebSocketHandler

import config
from utils import tools
from utils.captcha import captcha
from utils.response_code import RET, error_map
from utils.tools import object_to_str


class BaseHandler(RequestHandler):
    """自定义基类"""
    def get_numset(self):
        nums = self.db.query('select * from twsix_numset')
        numset = {}
        for i in nums:
            numset[i['num']] = {
                'class': i['class'],
                'shengxiao': i['shengxiao']
            }
        return numset
    def gen_hash_string(self, user_id):

        return uuid.uuid5(uuid.NAMESPACE_DNS, str(user_id)).hex

    def check_xsrf_cookie(self):
        '''此处不做xsrf认证，在需要的handler中设置'''
        pass

    @property
    def db(self):
        """作为RequestHandler对象的db属性"""
        return self.application.db

    @property
    def redis(self):
        """作为RequestHandler对象的redis属性"""
        return self.application.redis

    @property
    def local_ip(self):
        '''
        获取本机ip
        :return:
        '''
        return socket.gethostbyname(socket.getfqdn(socket.gethostname()))

    def prepare(self):
        """预解析json数据"""
        if self.request.headers.get("Content-Type", "").startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = {}

    def return_permission_error(self, msg=None):
        '''
        权限不足
        :return:
        '''
        return self.write({'code': RET.PERMISSIONERR, 'msg': msg or error_map[RET.PERMISSIONERR]})

    def return_req_error(self, msg=None):
        return self.write(dict(code=RET.REQERR, msg=msg or error_map[RET.REQERR]))

    def return_ok(self, **kwargs):
        '''
        操作完成
        :return:
        '''
        res = {'status': '1','info':'成功','time':str(int(time.time()))}
        kwargs and res.update(kwargs)
        if kwargs:
            res = object_to_str(res)
        return self.write(res)

    def return_db_error(self):
        '''
        数据库操作错误
        :return:
        '''
        return self.write({'code': RET.DBERR, 'msg': error_map[RET.DBERR]})

    def return_user_error(self):
        '''
        用户认证失败
        :return:
        '''
        return self.write({'code': RET.USERERR, 'msg': error_map[RET.USERERR]})

    def return_parameter_error(self, msg=''):
        '''参数错误'''
        return self.write({'code': RET.PARAMERR, 'msg': msg or error_map[RET.PARAMERR]})

    def return_unknow_error(self):
        '''
        返回未知错误
        :return:
        '''
        return self.write({'code': RET.UNKOWNERR, 'msg': error_map[RET.UNKOWNERR]})

    def return_data_exist(self, msg=''):
        '''
        返回数据已经存在
        :return:
        '''
        return self.write({'code': RET.DATAEXIST, 'msg': msg or error_map[RET.DATAEXIST]})

    def return_data_not_exist(self, msg=''):
        '''
        返回数据不存在
        :return:
        '''
        return self.write({'code': RET.NODATA, 'msg': msg or error_map[RET.NODATA]})

    def return_server_error(self):
        '''服务器内部错误'''
        return self.write(dict(code=RET.SERVERERR, msg="SERVERERR"))


    async def curl_http(self,url):
        base_url  = 'https://686tk.com/#/'
        print('url ==== ',url)
        print('request ==== ',self.request.__dict__)


        http_client = AsyncHTTPClient()
        try:
            uri = self.request.uri
            print('uri ==== ',uri)
            if not uri:
                uri = '/#/'

            # 用json方式提交是为了防止 content中有&字符
            request = HTTPRequest(url=base_url,
                                  method='GET',
                                  headers=self.request.headers,
                                  # body=parse.urlencode(data).encode('utf-8')
                                  )
            print(self.request.arguments)
            # if self.request.method == 'get':
            #     request = HTTPRequest(url=base_url + uri,
            #                           method=self.request.method,
            #                           headers=self.request.headers,
            #                           )

            response = await http_client.fetch(request)

            print(response.body)
            return response
        except Exception as e:
            traceback.print_exc()
            print("Error: %s" % e)
            return None





class AuthBaseHandler(BaseHandler):

    def prepare(self):
        super(AuthBaseHandler, self).prepare()
        self.get_current_user()
        if not self.token_data:
            self.send_error(404)
            return

    def get_current_user(self):
        #  上传文件使用element ui 的上传组件，添加data参数，避免网页版跨域问题
        # self.get_cookie('token')              游客token
        # self.get_secure_cookie('customer_token')   客服网页版cookie
        token = self.get_cookie('token') \
                or self.get_secure_cookie('customer_token') \
                or self.get_argument('customer_token', '') \
                or self.request.headers.get('token')\
                or self.get_argument('token','')
        try:
            self.token_data = jwt.decode(token, config.JWT_CUSTOMER_SECRET_KEY, algorithms='HS256')
        except Exception as e:
            # 扫码用户
            try:
                self.token_data = jwt.decode(token, config.JWT_TOURIST_SECRET_KEY, algorithms='HS256')
            except Exception as e:
                # 后台上传用户图片
                token = self.get_argument('upload_token', '')
                try:
                    self.token_data = jwt.decode(token, config.JWT_ADMIN_SECRET_KEY, algorithms='HS256')
                except Exception as e:
                    self.token_data = {}
        return self.token_data


class UploadImg(AuthBaseHandler):

    def options(self):
        pass

    def set_default_headers(self):
        """设置默认json格式"""
        self.set_header("Access-Control-Allow-Origin", 'http://localhost:9099')
        # 允许携带身份信息
        self.set_header("Access-Control-Allow-Credentials", 'true')
        # 对于允许域名不为*的必须手动指定允许请求头
        self.set_header("Access-Control-Allow-Headers",
                        "Accept,Content-Type,Referer,Sec-Fetch-Dest,User-Agent,header_auth,"
                        "token,customer_token")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS,DELETE,PUT")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    async def post(self, *args, **kwargs):
        if not self.get_current_user():
            return self.write(dict(code=RET.USERERR, msg=error_map[RET.USERERR]))
        try:

            # 根据files获取到的文件是列表格式
            img_file = self.request.files['file'][0]
            # 文件名
            file_original_name = img_file['filename']
            # 上传类型，有头像和聊天图片两种
            img_type = self.get_argument('type', 'img')

            # 判断文件格式
            file_type = file_original_name.split('.')[-1]
            if file_type not in ['jpg', 'png', 'bmp', 'webp', 'gif', 'tiff','jpeg']:
                return self.write(dict(code=RET.PARAMERR, msg=error_map[RET.PARAMERR]))

            # 上传的文件的二进制数据
            file_data = img_file['body']

            timestrmp = '{}.{}'.format(int(time.time() * 1000), file_type)
            day_folder = time.strftime('%Y%m%d')

            # 文件保存路径
            local_file_path = os.path.join(config.UPLOAD_IMG_ROOT if img_type == 'img' else config.UPLOAD_AVATAR_ROOT,
                                           day_folder)
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            # 保存文件到本地
            local_file_path = os.path.join(local_file_path, timestrmp)
            with open(local_file_path, 'wb') as f:
                f.write(file_data)

            img_src = os.path.join('/public/', img_type, day_folder, timestrmp).replace('\\', '/')
            return self.write({
                'code': 0,
                'msg': '',
                'data': {
                    'src': img_src
                }
            })
        except Exception as e:
            logging.error('图片上传失败{}'.format(self.token_data['name']))
            traceback.print_exc()
            return self.write(dict(code=RET.PARAMERR, msg=error_map[RET.PARAMERR]))


class UploadFile(AuthBaseHandler):

    def options(self):
        pass

    def set_default_headers(self):
        """设置默认json格式"""
        self.set_header("Access-Control-Allow-Origin", 'http://localhost:9099')
        # 允许携带身份信息
        self.set_header("Access-Control-Allow-Credentials", 'true')
        # 对于允许域名不为*的必须手动指定允许请求头
        self.set_header("Access-Control-Allow-Headers",
                        "Accept,Content-Type,Referer,Sec-Fetch-Dest,User-Agent,header_auth,"
                        "token,customer_token")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS,DELETE,PUT")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    async def post(self, *args, **kwargs):
        if not self.get_current_user():
            return self.write(dict(code=RET.USERERR, msg=error_map[RET.USERERR]))
        try:

            # 根据files获取到的文件是列表格式
            img_file = self.request.files['file'][0]
            # 文件名
            file_original_name = img_file['filename']

            # 文件格式
            file_type = file_original_name.split('.')[-1]
            img_type = 'file'
            # 上传的文件的二进制数据
            file_data = img_file['body']

            timestrmp = '{}.{}'.format(int(time.time() * 1000), file_type)
            day_folder = time.strftime('%Y%m%d')

            # 文件保存路径
            local_file_path = os.path.join(config.PROJECT_ROOT,'public','file',
                                           day_folder)
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            # 保存文件到本地
            local_file_path = os.path.join(local_file_path, timestrmp)
            with open(local_file_path, 'wb') as f:
                f.write(file_data)

            img_src = os.path.join('/public/', img_type, day_folder, timestrmp).replace('\\', '/')
            return self.write({
                'code': 0,
                'msg': '',
                'data': {
                    'src': img_src
                }
            })
        except Exception as e:
            logging.error('图片上传失败{}'.format(self.token_data['name']))
            traceback.print_exc()
            return self.write(dict(code=RET.PARAMERR, msg=error_map[RET.PARAMERR]))


class HtmlPageHandler(BaseHandler):

    def set_default_headers(self):
        self.set_header('Content-Type', 'text/html;charset=utf-8')


class AdminPicCodeHandler(BaseHandler):
    """图片验证码"""

    def get(self):
        """获取图片验证码"""
        # 验证码序号
        vernum = int(self.get_query_argument('vernum', 0))
        # 没有验证码序号
        if not vernum:
            return self.return_parameter_error()
        # 获取请求ip
        if config.settings['debug']:
            # debug模式下不启用nginx使用这种
            ip = self.request.remote_ip
        else:
            # nginx 转发后使用x-real-ip
            ip = self.request.headers.get('x-real-ip')
        # 生成图片验证码
        name, text, pic = captcha.captcha.generate_captcha()
        try:
            # 验证码保存到redis中
            text = text.upper()
            self.redis.set_verify_code(vernum=vernum, ip=ip, code=text)
        except Exception as e:
            logging.error(e)
        else:
            self.set_header("Content-Type", "image/jpg")
            self.write(pic)


class StaticFileBaseHandler(StaticFileHandler):
    """自定义静态文件处理类, 在用户获取html页面的时候设置_xsrf的cookie"""

    def __init__(self, *args, **kwargs):
        super(StaticFileBaseHandler, self).__init__(*args, **kwargs)
