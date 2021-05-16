# -*- encoding: utf-8 -*-
"""
@File    : urls.py
@Time    : 2020/8/31 21:57
@Author  : Perry
@Email   : 3500396415@qq.com
@Software: PyCharm
"""
import os

from tornado.web import StaticFileHandler

from handler import indexhandler, adminhandler, basehandler

urls = [
    (r'/', indexhandler.Index),
    (r'/htadmin', indexhandler.HtAdmin),
    (r'/config', indexhandler.Config),
    (r"/static/(.*)", indexhandler.StaticHandler,),
    (r"/pages/webview/(.*)", indexhandler.WebviewHandler,),

    (r"/pages/tie/(\d{1,10})", indexhandler.Tie,),
    (r"/statics/(.*)", StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "static"), default_filename="index.html")),

    (r'/admin/login', indexhandler.AdminLogin),
    (r'/api/uploadImg', adminhandler.AdminUpPic),
    (r'/api/vercode', basehandler.AdminPicCodeHandler),
    (r'/api/login', adminhandler.AdminLoginHandler),
    (r"/api/tie", adminhandler.Tie),
    (r"/api/tieInfo", adminhandler.TieInfo),
    (r'/api/user/info', adminhandler.AdminUserInfo),
    (r'/api/lottery/nums/list', adminhandler.AdminNums),
    (r'/api/lottery/nums', adminhandler.AdminNums),
    (r'/api/lottery/history', adminhandler.AdminLotteryHistory),
    (r'/api/lottery', adminhandler.AdminLottery),
    (r'/api/lottery/money', adminhandler.AdminLotteryMoney),
    (r'/api/admin/password', adminhandler.AdminPassword),
    (r'/api/user/logout', adminhandler.AdminLogout),
    # (r"/static/(.*)", StaticFileHandler,
    #  dict(path=os.path.join(os.path.dirname(__file__), "static"), default_filename="index.html"))

]
