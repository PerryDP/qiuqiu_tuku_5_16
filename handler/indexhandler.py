# -*- encoding: utf-8 -*-
"""
@File    : indexhandler.py
@Time    : 2020/8/31 22:35
@Author  : Perry
@Email   : 3500396415@qq.com
@Software: PyCharm
"""
import datetime
import json
import re
import traceback
from pprint import pprint

import math
import time

from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from handler.basehandler import BaseHandler


class Index(BaseHandler):

    async def get(self):
        return self.render('home.html')
        # return self.render('index.html')
        # return self.write('111111')


class HtAdmin(BaseHandler):

    def get(self):
        return self.render('index.html')

class Config(BaseHandler):

    async def get(self):
        '''
        原始数据
        {"msg":"操作成功","code":200,"data":{"widget_url":"https://kxl6.com","chat_room_notice":"这是聊天室公告",
        "openChatRoom":"0","app_version":"3.1.2","year":2021,
        "next_issue":92,"chat_room_name":"686图库交流",
        "next_issue_xg":25,"sites":[],"next_issue_time_xg":"2021-04-02 21:32:00",
        "tuku_collection_tip":"686图库易记网址<span style=\"color:red\">686tk.com</span>请收藏，永不迷路~",
        "openSignIn":false,"issue_tw":35,"resource_domain":"https://s.686tk.com",
        "tuku_forum_url":"https://686tk.com","app_version_info":"1、更新了xxx;2、新增xyz",
        "withdrawUser":{"nickname":"686图库管理员","id":0},"next_issue_tw":36,
        "tuku_forum_intro":"</font>全网推荐<font color=\"#FF0000\">【再次爆庄一码】</font><font color=\"#0000FF\">已连中</font></a>",
        "no_talk":"0","issue":91,"ios_url":"https://kxl6.com","adver":{"gmt_create":"2020-07-03 00:02:17","jump_url":null,
        "is_on":true,"id":1,"type":"无跳转","url":"https://changliao.agao88.com/amtk/img/32967673ff974482a4d0d814fe153716.jpg","timeout":"5"},
        "next_issue_time":"2021-04-02 21:34:00","next_issue_time_tw":"2021-04-02 20:50:00","openTw":"0","issue_xg":24,
        "android_url":"https://kxl6.com","gaoshou_ziliao_url":"https:686tk.com"},"success":true}

        :return:
        '''
        # Content-Type:
        #
        # application/json; charset=utf-8
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        # https://api.686tk.com/config
        http_client = AsyncHTTPClient()
        try:

            # 用json方式提交是为了防止 content中有&字符
            request = HTTPRequest(url='https://api.686tk.com/config',
                                  method='GET',
                                  )
            response = await http_client.fetch(request)
            json_data = json.loads(response.body)
            # pprint(json_data)
            json_data['data']['widget_url'] = 'https://187708.com'
            json_data['data']['android_url'] = 'https://187708.com'
            json_data['data']['ios_url'] = 'https://187708.com'
            json_data['data']['tuku_forum_url'] = 'https://5688tk.com'
            json_data['data']['adver'] = {'gmt_create': '2020-07-03 00:02:17',
                    'id': 1,
                    'is_on': True,
                    'jump_url': None,
                    'timeout': '5',
                    'type': '无跳转',
                    'url': ''}
            json_data['data']['withdrawUser'] = {
                'id': 0, 'nickname': '5688图库管理员'
            }
            json_data['data']['tuku_collection_tip'] = '5688图库易记网址<span style="color:red">5688tk.com</span>请收藏，永不迷路~'
            return self.write(json.dumps(json_data))
        except Exception as e:
            traceback.print_exc()
            return




class StaticHandler(BaseHandler):

    async def get(self, *args):
        print(args)
        if(args[0].find('logo') > -1):

            print('logo 图片=== ',args[0])


        http_client = AsyncHTTPClient()



        url = f'https://686tk.com/{self.request.uri}'
        response = await http_client.fetch(url)

        # print('response body',response.body)
        for key, v in response.headers.items():
            self.set_header(key, v)

        return self.write(response.body)


class WebviewHandler(BaseHandler):

    def get(self, *args):
        tuku = self.db.query('select * from tuku_tie order by id desc ')

        return self.render('tieList.html', tuku=tuku)


class Tie(BaseHandler):

    def get(self, t_id):
        tie = self.db.get('select * from tuku_tie where id = %s ', t_id)
        return self.render('tieContent.html', tie=tie)


class Xixi(BaseHandler):

    def get(self):
        '''
        banner页面
        仿原站的，真他妈垃圾架构。
        :return:
        '''
        banners = self.db.query('select * from twsix_banner')
        self.render('index/xixi.html', banners=banners)


class MaHuiJianJie(BaseHandler):

    def get(self):
        '''
        马会简介页面
        仿原站的，真他妈垃圾架构。
        :return:
        '''

        self.render('index/mahuijianjie.html')


class NewsInfo(BaseHandler):

    def post(self):
        '''
        下期开奖数据
        data: {1204: {nextIssue: "2020245", shengxiao: "兔,兔,牛,蛇,猪,虎,蛇", nextTime: 1598967180, issue: "2020244",…}}
        1204: {nextIssue: "2020245", shengxiao: "兔,兔,牛,蛇,猪,虎,蛇", nextTime: 1598967180, issue: "2020244",…}
        DAOJISHI: 2525030
        issue: "2020244"
        nextIssue: "2020245"
        nextTime: 1598967180
        number: "34,10,24,08,02,11,32"
        shengxiao: "兔,兔,牛,蛇,猪,虎,蛇"
        info: "成功"
        status: "1"
        time: 1596442150
        :return:
        '''

        next_info = \
            self.db.query('select next_issue,unix_timestamp(`next_time`) as next_time ,next_time as next_date_time,'
                          'next_2_issue,unix_timestamp(`next_2_time`) as next_2_time,next_2_time as next_2_date_time,'
                          ' nums,shengxiaos '
                          ' from twsix_next ')[0]

        # 判断时间 小于 1毫秒
        now = int(time.time())
        print('now ====', now)
        print('now date ===', datetime.datetime.fromtimestamp(now))
        print('now date ===', datetime.datetime.now())
        print('next === ', next_info)
        print('开奖时间 === ', next_info['next_date_time'])
        print('开奖时间 ===+120= ', next_info['next_time'] + 120)
        print("next_info['next_time'] + 120 - now < 10 ===", next_info['next_time'] + 120 - now < 10)

        if next_info['next_2_issue'] and next_info['next_time'] and next_info['next_2_time'] \
                and next_info['next_time'] + 120 - now < 10 and next_info['next_2_issue'] > next_info['next_issue']:
            try:
                # 查看最新的数据
                self.db.execute('update twsix_next set next_issue=%s,next_time=%s,next_2_issue=%s,next_2_time=%s,'
                                'nums=%s,shengxiaos=%s', next_info['next_2_issue'], next_info['next_2_date_time'],
                                str(int(next_info['next_2_issue']) + 1), None, '', '')
                # 插入最新的数据
                self.db.insert(
                    'insert into twsix_history(`issue`,`nums`,`shengxiaos`,`create_at`) values (%s,%s,%s,%s)',
                    next_info['next_issue'], next_info['nums'], next_info['shengxiaos'],
                    next_info['next_date_time'])
                prev_info = {
                    'issue': next_info['next_issue'],
                    'shengxiaos': next_info['shengxiaos'],
                    'nums': next_info['nums']
                }
                next_info['next_issue'] = next_info['next_2_issue']
                next_info['next_time'] = next_info['next_2_time']
            except Exception as e:
                prev_info = self.db.get('select * from twsix_history order by issue desc limit 1 offset 0 ')

        else:
            prev_info = self.db.get('select * from twsix_history order by issue desc limit 1 offset 0 ')
        data = {
            "1204": {
                "nextIssue": next_info['next_issue'],
                "nextTime": next_info['next_time'] + 120,  # 加2分钟
                "issue": prev_info['issue'],
                "shengxiao": prev_info['shengxiaos'],
                "number": prev_info['nums'],
                "DAOJISHI": next_info['next_time'] - int(time.time())
            }
        }

        return self.return_ok(data=data)


class HistoryInfo(BaseHandler):

    def post(self):
        '''
        历史数据
        {"time":1596442058,
        "status":"1",
        "data":{"pageSize":45,
                "list":
                    [{"time":"2020-09-01 21:30:00","numberstr":"28,27,02,10,05,18,30","shengxiao":"鸡,狗,猪,兔,猴,羊,羊","issue":"2020245"},
                    {"time":"2020-08-31 21:30:00","numberstr":"34,10,24,08,02,11,32","shengxiao":"兔,兔,牛,蛇,猪,虎,蛇","issue":"2020244"}
                    ],
                "totalSize":245,
                "pageNum":1},
        "info":"成功"}
        :return:
        '''
        page_num = self.json_args['data']['pageNum']
        page_size = self.json_args['data']['pageSize']

        now = time.time()

        data = {
            'pageSize': 0,
            'list': [],
            'totalSize': 0,
            'pageNum': page_num,
        }
        count = self.db.get('select count(*) as count from twsix_history')['count']
        if not count:
            return self.return_ok(time=now, data=data)
        # 计算分页数
        page_count = math.ceil(count / page_size)
        if page_num > page_count:
            page_num = page_count
        elif page_num < 1:
            page_num = 1
        data['pageSize'] = page_count
        data['totalSize'] = count
        data['list'] = self.db.query(
            'select create_at as time,issue,nums as numberstr,shengxiaos as shengxiao from twsix_history '
            'order by issue desc '
            'limit %s '
            'offset %s ', page_size, (page_num - 1) * page_size)

        return self.return_ok(time=now, data=data)


class LotteryJs(BaseHandler):
    def money_format(self, value):
        # value = "%.2f" % float(value)
        if not isinstance(value, str):
            value = str(value)
        if value.replace('.', '').isdigit():
            value = '%.2f' % round(float(value), 2)
            components = str(value).split('.')
            if len(components) > 1:
                left, right = components
                right = '.' + right
            else:
                left, right = components[0], ''

            result = ''
            while left:
                result = left[-3:] + ',' + result
                left = left[:-3]
            return result.strip(',') + right

    def get(self):
        tuijian = self.db.query('select tuijian_nums from twsix_next ')[0]['tuijian_nums']
        if tuijian:
            tuijian = tuijian.split(',')
        else:
            tuiian = []
        money_data = self.db.query('select * from twsix_prev')[0]
        money_data['yi_money'] = self.money_format(money_data['yi_money'])
        money_data['er_money'] = self.money_format(money_data['er_money'])
        money_data['san_money'] = self.money_format(money_data['san_money'])
        return self.render('index/lottery.js', tuijian=tuijian, money_data=money_data)

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/javascript')


class AdminLogin(BaseHandler):

    def get(self):
        server_time = int(time.time()) * 1000
        return self.render('index.html', server_time=server_time)


#  ------------------外部调用-------------
class ExternalBaseHandler(BaseHandler):
    def check_time(self):
        '''
        :return:
        '''
        next_info = \
            self.db.query('select next_issue,unix_timestamp(`next_time`) as next_time ,next_time as next_date_time,'
                          'next_2_issue,unix_timestamp(`next_2_time`) as next_2_time,next_2_time as next_2_date_time,'
                          ' nums,shengxiaos '
                          ' from twsix_next ')[0]

        # 判断时间 小于 1毫秒
        now = int(time.time())

        if next_info['next_2_issue'] and next_info['next_time'] and next_info['next_2_time'] \
                and next_info['next_time'] + 120 - now < 10 and next_info['next_2_issue'] > next_info['next_issue']:
            try:
                # 查看最新的数据
                self.db.execute('update twsix_next set next_issue=%s,next_time=%s,next_2_issue=%s,next_2_time=%s,'
                                'nums=%s,shengxiaos=%s', next_info['next_2_issue'], next_info['next_2_date_time'],
                                str(int(next_info['next_2_issue']) + 1), None, '', '')
                # 插入最新的数据
                self.db.insert(
                    'insert into twsix_history(`issue`,`nums`,`shengxiaos`,`create_at`) values (%s,%s,%s,%s)',
                    next_info['next_issue'], next_info['nums'], next_info['shengxiaos'],
                    next_info['next_date_time'])
            except Exception as e:
                pass

    def prepare(self):
        '''
        :return:
        '''
        super(ExternalBaseHandler, self).prepare()

        self.check_time()


class ExternalNew(ExternalBaseHandler):

    def prepare(self):

        pass

    def get(self):
        '''
        外部调用最新开奖
        开奖当天9点钟到9点35分显示开奖中，
        :return:

        '''
        next_info = \
            self.db.query('select next_issue,unix_timestamp(`next_time`) as next_time ,next_time as next_date_time,'
                          'next_2_issue,unix_timestamp(`next_2_time`) as next_2_time,next_2_time as next_2_date_time,'
                          ' nums,shengxiaos '
                          ' from twsix_next ')[0]
        data = {}
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        # 检查下期开奖时间是否是今天
        date_now = datetime.datetime.now()
        next_date_time = next_info['next_date_time']
        if next_date_time and next_date_time.date() == date_now.date():
            # 时间是否是开奖时间 指定开奖时间为 21.33  ，则为21.00 到21.33 之间 实际加2分钟
            if date_now.hour == next_date_time.hour and date_now.minute < next_date_time.minute + 2:
                data['nums'] = list('台灣六合彩開獎')
                data['shengxiaos'] = ['&nbsp;' for i in range(7)]
                data['class'] = ['gray_' for i in range(7)]
                data['issue'] = next_info['next_issue'][-3:]
                data['next_issue'] = next_info['next_issue'][-3:]
                data['date'] = next_info['next_date_time'].strftime('%m %d').replace(' ', '月')
                data['week_day'] = week_day_dict[next_info['next_date_time'].weekday()]
                return self.render('external/new.html', data=data)
        self.check_time()

        prev_info = self.db.get('select * from twsix_history order by issue desc limit 1 offset 0 ')
        if prev_info:
            # 获取生肖
            numset = self.get_numset()
            data['nums'] = prev_info['nums'].split(',')
            data['shengxiaos'] = prev_info['shengxiaos'].split(',')

            data['class'] = []
            print('data_nums =-===', data['nums'])
            for i in data['nums']:
                data['class'].append(numset[i]['class'])
            data['issue'] = prev_info['issue'][-3:]
            next_info = self.db.query('select * from twsix_next ')[0]
            data['next_issue'] = next_info['next_issue'][-3:]
            data['date'] = next_info['next_time'].strftime('%m %d').replace(' ', '月')
            data['week_day'] = week_day_dict[next_info['next_time'].weekday()]
        else:
            return self.write('无数据')
        return self.render('external/new.html', data=data)


class ExternalHistory(ExternalBaseHandler):

    def get(self):
        '''
        历史数据
        :return:
        '''

        year = self.get_argument('year', str(datetime.datetime.now().year))
        # 验证year格式是否正确
        if not re.match(r'^\d{4}$', year):
            return self.write('请求参数不正确')
        db_data = self.db.query('select * from twsix_history where issue like concat(%s,"%%") order by issue desc ',
                                year)
        if not db_data:
            return self.write('暂无数据')

        data = {'year': year, 'items': []}
        numset = self.get_numset()
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期天',
        }
        for i in db_data:
            _data = {}
            _data['nums'] = i['nums'].split(',')
            _data['shengxiaos'] = i['shengxiaos'].split(',')
            _data['class'] = []
            for j in _data['nums']:
                _data['class'].append(numset[j]['class'])

            _data['issue'] = i['issue'][-3:]

            _data['date'] = i['create_at'].strftime('%Y-%m-%d')
            _data['week_day'] = week_day_dict[i['create_at'].weekday()]
            data['items'].append(_data)

        return self.render('external/history.html', data=data)
