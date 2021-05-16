# -*- encoding: utf-8 -*-
"""
@File    : adminhandler.py
@Time    : 2020/9/2 4:22
@Author  : Perry
@Email   : 3500396415@qq.com
@Software: PyCharm
"""
import datetime
import logging
import os
import time

import math
import traceback

import jwt
from jwt import ExpiredSignatureError

import config
from handler.basehandler import BaseHandler
from utils import tools
from utils.response_code import RET, error_map
from utils.tools import object_to_str


class AdminApiBaseHandler(BaseHandler):
    def set_default_headers(self):
        """设置默认json格式"""
        print('设置请求头')
        self.set_header("Access-Control-Allow-Origin", '*')
        # 允许携带身份信息
        self.set_header("Access-Control-Allow-Credentials", 'true')
        # 对于允许域名不为*的必须手动指定允许请求头
        self.set_header("Access-Control-Allow-Headers",
                        "Accept,Content-Type,Referer,Sec-Fetch-Dest,User-Agent,header_auth,"
                        "token,admin_token")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS,DELETE,PUT")
        self.set_header("Content-Type", "application/json; charset=UTF-8")

    def limit_page(self, count):

        max_page = math.ceil(count / self.limit)
        if self.page < 1:
            self.page = 1
        elif self.page > max_page:
            self.page = max_page

        self.offset = (self.page - 1) * self.limit

    def options(self):
        pass

    def return_ok(self, **kwargs):
        '''
        操作完成
        :return:
        '''
        res = {'code': 0}
        kwargs and res.update(kwargs)
        if kwargs:
            res = object_to_str(res)
        return self.write(res)

    def prepare(self):
        if self.request.method == 'OPTIONS':
            return
        #         检查token
        elif not self.get_current_user():
            self.return_permission_error()
            self.finish()
            return
        super(AdminApiBaseHandler, self).prepare()

        self.limit = int(self.get_argument('limit', 30))
        self.page = int(self.get_argument('page', 1))

    def get_current_user(self):
        token_str = self.get_cookie('admin_token', '') \
                    or self.request.headers.get('token', '') \
                    or self.get_argument('token', '')
        try:
            self.token_data = jwt.decode(token_str, config.JWT_ADMIN_SECRET_KEY, algorithms='HS256')
        except ExpiredSignatureError as e:
            # token 过期
            self.token_data = None
            traceback.print_exc()
        print('self token data ', self.token_data)
        return self.token_data


class AdminLoginHandler(BaseHandler):

    def return_ok(self, **kwargs):
        '''
        操作完成
        :return:
        '''
        res = {'code': 0}
        kwargs and res.update(kwargs)
        if kwargs:
            res = object_to_str(res)
        return self.write(res)

    def options(self):
        pass

    def set_default_headers(self):
        """设置默认json格式"""
        print('设置请求头')
        if config.IS_DEBUG:
            self.set_header("Access-Control-Allow-Origin", '*')
            # 允许携带身份信息
            self.set_header("Access-Control-Allow-Credentials", 'true')
            # 对于允许域名不为*的必须手动指定允许请求头
            self.set_header("Access-Control-Allow-Headers",
                            "Accept,Content-Type,Referer,Sec-Fetch-Dest,User-Agent,header_auth,"
                            "token,admin_token")
            self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS,DELETE,PUT")
            self.set_header("Content-Type", "application/json; charset=UTF-8")

    def set_jwt(self, user):
        # 生成jwt
        playload = {
            'pid': user['id'],
            'name': user['username'],
            'role': user['role'],
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=0,
                                                                   minutes=config.JWT_ADMIN_EXP_TIME,
                                                                   seconds=0),
        }
        # 全面改用jwt
        # 创建JWT
        token = jwt.encode(playload, config.JWT_ADMIN_SECRET_KEY, algorithm='HS256')
        self.set_cookie('admin_token', token.decode('utf8'), path='/')
        return token.decode('utf8')

    def post(self):
        '''
    roles: ['admin'],
    introduction: 'I am a super administrator',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Super Admin'

        :return:
        '''
        print('json_args == ', self.json_args)
        username = self.json_args['username']
        password = self.json_args['password']
        ip = self.request.remote_ip

        admin_info = self.db.get('select * from tuku_admin where username = %s', username)
        if not admin_info:
            return self.write(dict(code=400, msg='用户不存在或密码错误'))

        # 判断密码
        if not tools.generate_password(password + admin_info['salt']) == admin_info['password']:
            return self.write(dict(code=400, msg='用户不存在或密码错误'))

        token = self.set_jwt(admin_info)

        self.db.execute('insert into tuku_admin_login_history(`username`,`ip`) values (%s,%s)', username, ip)
        #     roles: ['admin'],
        #     introduction: 'I am a super administrator',
        #     avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        #     name: 'Super Admin'
        return self.return_ok(token=token)


class AdminUserInfo(AdminApiBaseHandler):

    def get(self):
        '''
        获取用户信息
        :return:  data =  roles: ['editor'],
    introduction: 'I am an editor',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Normal Editor'
        '''
        return self.return_ok(data={
            'roles': ['admin' if self.token_data['role'] == 1 else 'editor'],
            'introduction': '管理员',
            'avatar': '/statics/img/404_cloud.0f4bc32b.png',
            'name': self.token_data['name']
        })


class AdminUpPic(AdminApiBaseHandler):
    

    def post(self):
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
            # 文件保存路径
            local_file_path = os.path.join(config.PROJECT_ROOT,'static','img')
            if not os.path.exists(local_file_path):
                os.makedirs(local_file_path)
            # 保存文件到本地
            local_file_path = os.path.join(local_file_path, timestrmp)
            with open(local_file_path, 'wb') as f:
                f.write(file_data)

            img_src = os.path.join('/statics', img_type, timestrmp).replace('\\', '/')
            return self.write({
                'code': 0,
                'msg': '',
                'data': {
                    'src': f'{self.request.protocol}://{self.request.host}{img_src}'
                }
            })
        except Exception as e:
            logging.error('图片上传失败{}'.format(self.token_data['name']))
            traceback.print_exc()
            return self.write(dict(code=RET.PARAMERR, msg=error_map[RET.PARAMERR]))


class Tie(AdminApiBaseHandler):

    def get(self):
        '''
        获取帖子列表
        :return:
        '''

        where = ['true']
        title = self.get_argument('title', '')

        if title:
            where.append(f'title like concat("%%","{title}","%%")')
        where = ' and '.join(where)
        count = self.db.get('select count(*) as count  from tuku_tie where {}'.format(where))['count']

        if not count:
            return self.return_ok(data=[], total=0)

        self.limit_page(count)

        data = self.db.query('select * from tuku_tie  where {} order by id desc '.format(where))

        return self.return_ok(data=data, total=count)

    def delete(self):

        print('删除', self.json_args)

        tie_id = self.json_args['id']

        self.db.execute('delete from tuku_tie where id = %s ', tie_id)

        return self.return_ok()

    def put(self):
        print('json',self.json_args)
        print('arg',self.request.arguments)
        t_id = self.json_args.get('id', '')
        title = self.json_args['title']
        content = self.json_args['content']
        if t_id:
            # 修改
            self.db.execute('update tuku_tie set title = %s  ,content = %s where id = %s ', title, content,t_id)
        else:
            # 创建
            self.db.execute('insert into tuku_tie(`title`,`content`) values (%s,%s )', title, content)
        return self.return_ok()
        #


class TieInfo(AdminApiBaseHandler):

    def get(self):
        t_id = self.get_argument('id')

        data = self.db.get('select * from tuku_tie where id = %s ', t_id)
        return self.return_ok(data=data)


class AdminNums(AdminApiBaseHandler):

    def get(self):
        '''

        :return:
        '''

        nums = self.db.query('select * from twsix_numset ')
        if not nums:
            nums = [[1, '01', 'red_', '鼠'], [2, '02', 'red_', '豬'], [3, '03', 'blue_', '狗'], [4, '04', 'blue_', '雞'],
                    [5, '05', 'green_', '猴'], [6, '06', 'green_', '羊'], [7, '07', 'red_', '馬'], [8, '08', 'red_', '蛇'],
                    [9, '09', 'blue_', '龍'], [10, '10', 'blue_', '兔'], [11, '11', 'green_', '虎'],
                    [12, '12', 'red_', '牛'], [13, '13', 'red_', '鼠'], [14, '14', 'blue_', '豬'],
                    [15, '15', 'blue_', '狗'],
                    [16, '16', 'green_', '雞'],
                    [17, '17', 'green_', '猴'], [18, '18', 'red_', '羊'], [19, '19', 'red_', '馬'],
                    [20, '20', 'blue_', '蛇'],
                    [21, '21', 'green_', '龍'], [22, '22', 'green_', '兔'], [23, '23', 'red_', '虎'],
                    [24, '24', 'red_', '牛'],
                    [25, '25', 'blue_', '鼠'], [26, '26', 'blue_', '豬'], [27, '27', 'green_', '狗'],
                    [28, '28', 'green_', '雞'],
                    [29, '29', 'red_', '猴'], [30, '30', 'red_', '羊'], [31, '31', 'blue_', '馬'],
                    [32, '32', 'green_', '蛇'],
                    [33, '33', 'green_', '龍'], [34, '34', 'red_', '兔'], [35, '35', 'red_', '虎'],
                    [36, '36', 'blue_', '牛'],
                    [37, '37', 'blue_', '鼠'], [38, '38', 'green_', '豬'], [39, '39', 'green_', '狗'],
                    [40, '40', 'red_', '雞'],
                    [41, '41', 'blue_', '猴'], [42, '42', 'blue_', '羊'], [43, '43', 'green_', '馬'],
                    [44, '44', 'green_', '蛇'],
                    [45, '45', 'red_', '龍'], [46, '46', 'red_', '兔'], [47, '47', 'blue_', '虎'],
                    [48, '48', 'blue_', '牛'],
                    [49, '49', 'green_', '鼠']]
            self.db.executemany('insert into twsix_numset(`id`,`num`,`class`,`shengxiao`) values (%s,%s,%s,%s)', nums)

        return self.return_ok(data={
            'total': len(nums),
            'items': nums
        })

    def put(self):
        shengxiao = self.get_argument('shengxiao')
        num_id = int(self.get_argument('id'))
        shengxiaos = '鼠牛虎兔龍蛇馬羊猴雞狗豬鼠牛虎兔龙蛇马羊猴鸡狗猪'
        if shengxiao not in shengxiaos:
            return self.return_parameter_error(msg='生肖不合法')

        self.db.update('update twsix_numset set shengxiao  =  %s where id = %s', shengxiao, num_id)
        return self.return_ok()


class AdminLotteryHistory(AdminApiBaseHandler):

    def get(self):
        '''
        历史开奖信息
        :return:
        '''
        where = ['true']
        issue = self.get_argument('issue', '')
        print('self.json_args ', self.json_args)
        if issue:
            where.append(f'issue = "{issue}"')

        where = ' and '.join(where)
        count = self.db.get('select count(*) as count from twsix_history where {}'.format(where))['count']

        if not count:
            return self.return_ok(data=dict(total=0, items=[]))

        #         计算分页
        self.limit_page(count)

        items = self.db.query('select * from twsix_history where {} '
                              'order by issue desc '
                              'limit %s '
                              'offset %s '.format(where), self.limit, self.offset)
        return self.return_ok(data=dict(total=count, items=items))

    def set_nums_shengxiao(self, nums):
        shengxiaos = []
        numset = self.get_numset()
        for i in range(7):
            if len(nums[i]) < 2:
                # 单位数字补零
                try:
                    nums[i] = '0' + str(int(nums[i]))
                except Exception as e:
                    return self.return_parameter_error(msg='号码必须为数字')
            elif len(nums[i]) > 2:
                return self.return_parameter_error(msg='号码不合法')
            shengxiaos.append(numset[nums[i]]['shengxiao'])
        return ','.join(nums), ','.join(shengxiaos)

    def put(self):
        item = self.json_args
        nums = item['nums'].split(',')
        # 检查号码
        if len(nums) != 7:
            return self.return_parameter_error(msg='号码和生肖必须为7位且英文逗号隔开')
        item['nums'], item['shengxiaos'] = self.set_nums_shengxiao(nums)
        item['create_at'] = datetime.datetime.strptime(item['create_at'], '%Y-%m-%d %H:%M:%S')

        self.db.execute('update twsix_history set issue = %(issue)s,nums=%(nums)s,shengxiaos=%(shengxiaos)s,'
                        'create_at=%(create_at)s where id =%(id)s', **item)
        return self.return_ok(data=item)

    def post(self):
        item = self.json_args
        nums = item['nums'].split(',')
        # 检查号码
        if len(nums) != 7:
            return self.return_parameter_error(msg='号码和生肖必须为7位且英文逗号隔开')
        item['nums'], item['shengxiaos'] = self.set_nums_shengxiao(nums)
        item['create_at'] = datetime.datetime.strptime(item['create_at'], '%Y-%m-%d %H:%M:%S')

        item['id'] = self.db.execute(
            'insert into twsix_history(`issue`,`nums`,`shengxiaos`,`create_at`) values (%(issue)s,%(nums)s,%(shengxiaos)s,%(create_at)s)',
            **item)
        return self.return_ok(data=item)

    def delete(self):

        ids = self.json_args['ids']

        self.db.executemany('delete from twsix_history  where id = %s', ids)
        return self.return_ok()


class AdminLottery(AdminApiBaseHandler):
    def set_nums_shengxiao(self, nums):
        shengxiaos = []
        numset = self.get_numset()
        for i in range(7):
            if len(nums[i]) < 2:
                # 单位数字补零
                try:
                    nums[i] = '0' + str(int(nums[i]))
                except Exception as e:
                    return self.return_parameter_error(msg='号码必须为数字')
            elif len(nums[i]) > 2:
                return self.return_parameter_error(msg='号码不合法')
            shengxiaos.append(numset[nums[i]]['shengxiao'])
        return ','.join(nums), ','.join(shengxiaos)

    def get(self):
        '''

        :return:
        '''
        data = self.db.query('select * from twsix_next ')[0]
        return self.return_ok(data=data)

    def put(self):

        data = self.json_args
        # 设置生肖
        print(data)
        if data['nums']:
            nums = data['nums'].split(',')
            if len(nums) != 7:
                return self.return_parameter_error(msg='开奖号码必须为7个数字，英文逗号隔开')

            data['nums'], data['shengxiaos'] = self.set_nums_shengxiao(nums)

        #
        tuijian_nums = data['tuijian_nums']
        if tuijian_nums:
            tuijian_nums = tuijian_nums.split(',')
            for i in range(len(tuijian_nums)):
                if len(tuijian_nums[i]) < 2:
                    tuijian_nums[i] = '0' + tuijian_nums[i]
            data['tuijian_nums'] = ','.join(tuijian_nums)

        self.db.execute('update twsix_next set next_issue =%(next_issue)s,next_time  =  %(next_time)s,'
                        'next_2_issue=%(next_2_issue)s,next_2_time = %(next_2_time)s,tuijian_nums=%(tuijian_nums)s,'
                        'nums=%(nums)s,shengxiaos=%(shengxiaos)s', **data)
        return self.return_ok()


class AdminLotteryMoney(AdminApiBaseHandler):

    def get(self):
        '''

        :return:
        '''
        data = self.db.query('select * from twsix_prev ')[0]
        return self.return_ok(data=data)

    def put(self):
        data = self.json_args

        self.db.execute(
            'update twsix_prev set yi_money=%(yi_money)s,yi_nums=%(yi_nums)s,'
            'er_money=%(er_money)s,er_nums=%(er_nums)s,san_money=%(san_money)s,san_nums=%(san_nums)s', **data)

        return self.return_ok()


class AdminPassword(AdminApiBaseHandler):

    def put(self):
        # old_pwd ,new_pwd,con_pwd
        old_pwd = self.json_args['old_pwd']
        new_pwd = self.json_args['new_pwd']
        con_pwd = self.json_args['con_pwd']

        if new_pwd != con_pwd:
            return self.return_parameter_error(msg='两次密码不一致')

        # 验证密码
        admin = self.db.get('select * from twsix_admin where id = %s', self.token_data['pid'])

        # 判断密码
        if not tools.generate_password(old_pwd + admin['salt']) == admin['password']:
            return self.write(dict(code=400, msg='密码错误'))

        salt = tools.get_random_str(char=6)

        new_pwd = tools.generate_password(new_pwd + salt)

        self.db.execute('update twsix_admin  set password = %s ,salt = %s where id =%s', new_pwd, salt,
                        self.token_data['pid'])
        return self.return_ok()


class AdminLogout(AdminApiBaseHandler):

    def post(self):
        return self.return_ok()
