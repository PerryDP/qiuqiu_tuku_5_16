# coding:utf-8

class RET:
    OK                  = 0

    DBERR               = 4001
    NODATA              = 4002
    DATAEXIST           = 4003
    DATAERR             = 4004
    TOKENERR            = 4101
    LOGINERR            = 4102
    PARAMERR            = 4103
    USERERR             = 4104
    ROLEERR             = 4105
    PWDERR              = 4106      # 密码错误
    RESTRICTLOING       = 4107
    VERCODEERROR        = 4108
    WSCONNECTERR        = 4109      # ws连接不存在

    SAMENAME            = 6002      # 备注名字相同
    MOVESAMEGROUP       = 6003      # 移动为相同的分组
    SAMEGROUP           = 6004      # 命名分组为相同的名字（除我的好友之外）
    CANTUPDATE          = 6005      # 分组为（我的好友）不能修改
    ALREADYESISTGROUP   = 6006      # 分组已经存在了
    CANTDELETE          = 6007      # 分组为（我的好友）不能删除

    PERMISSIONERR       = 4200
    REQERR              = 4201
    IPERR               = 4202
    THIRDERR            = 4301
    IOERR               = 4302
    SERVERERR           = 4500
    UNKOWNERR           = 4501
    REPEAT_LOGIN        = 4600
    USERINIT            = 1000      # 会员初始化

    SYSTEM_MSG          = 2001      # 系统消息
    FRIEND_MSG          = 2002      # 好友消息
    GROUP_MSG           = 2003      # 群组消息

    # NOT_FRIEND          = 3401      # 不是自己的好友
    # FRIEND_ISIGNORE     = 3402      # 已屏蔽的好友
    # FRIEND_ISDELETE     = 3403      # 已删除的好友
    # RECEIVER_ISIGNORE   = 3404      # 被好友屏蔽
    # RECEIVER_ISDELETE   = 3405      # 被好友删除

    FRIEND_ISIGNORE     = 3401      # 已屏蔽的好友
    FRIEND_ISDELETE     = 3402      # 已删除的好友
    RECEIVER_ISIGNORE   = 3403      # 被好友屏蔽
    RECEIVER_ISDELETE   = 3404      # 被好友删除
    NOT_MY_FRIEND       = 3405      # 不是自己的好友，且自己设置不接受临时会话
    NOT_REC_FRIEND      = 3406      # 不是对方的好友，且对方设置不接受临时会话



error_map = {
    RET.OK                    : "成功",
    RET.USERINIT              : "会员初始化",
    RET.DBERR                 : "数据库查询错误",
    RET.NODATA                : "无数据",
    RET.DATAEXIST             : "数据已存在",
    RET.DATAERR               : "数据错误",
    RET.TOKENERR              : "用户未登录",
    RET.LOGINERR              : "用户登录失败",
    RET.PARAMERR              : "参数错误",
    RET.USERERR               : "用户不存在或未激活",
    RET.ROLEERR               : "用户身份错误",
    RET.PWDERR                : "密码错误",
    RET.RESTRICTLOING         : "限制登录",
    RET.VERCODEERROR          : '验证码错误',
    RET.PERMISSIONERR         : '权限不足，无法操作',
    RET.REQERR                : "非法请求或请求次数受限",
    RET.IPERR                 : "IP受限",
    RET.THIRDERR              : "第三方系统错误",
    RET.IOERR                 : "文件读写错误",
    RET.SERVERERR             : "内部错误",
    RET.UNKOWNERR             : "未知错误",
    RET.REPEAT_LOGIN          : "重复登录",

    RET.FRIEND_ISIGNORE       : '已屏蔽的好友',
    RET.FRIEND_ISDELETE       : '已删除的好友',
    RET.RECEIVER_ISIGNORE     : '被好友屏蔽',
    RET.RECEIVER_ISDELETE     : '被好友删除',
    RET.NOT_MY_FRIEND         : '不是自己的好友，且自己设置不接受临时会话',
    RET.NOT_REC_FRIEND        : '不是对方的好友，且对方设置不接受临时会话',

    RET.SAMENAME              : u'备注名字相同',
    RET.MOVESAMEGROUP         : u"移动到分组名字相同(未移动)",
    RET.SAMEGROUP             : u"分组名字相同",
    RET.CANTUPDATE            : u"默认的分组不能修改",
    RET.ALREADYESISTGROUP     : u"已经存在的分组，请重新命名",
    RET.CANTDELETE            : u"默认的分组不能删除"
}
