--
CREATE TABLE `tuku_admin` (
  `id` int auto_increment primary key ,
  `username` varchar(20) UNIQUE COMMENT '登录名',
  `password` varchar(100)  COMMENT '密码',
  `salt` char(6) comment '盐值',
  `locked` tinyint(1) DEFAULT 0 COMMENT '禁用(0:否,1:禁用)',
  `role` int default 0 comment '角色id',
  `last_time` datetime COMMENT '最近登录时间',
  `create_at` datetime DEFAULT now() COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
-- admin登录记录
CREATE TABLE `tuku_admin_login_history` (
  `id` int auto_increment primary key ,
  `username` varchar(20)  NOT NULL COMMENT '帐号',
  `ip` varchar(20) NOT NULL COMMENT '登录ip',
  `create_at` datetime DEFAULT now() COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

CREATE TABLE `tuku_tie` (
  `id` int auto_increment primary key ,
  `title` text comment '标题富文本',
  `content` text comment '内容富文本',
  `create_at` datetime default now() comment '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
CREATE TABLE `tuku_notice` (
  `id` int auto_increment primary key ,
  `content` varchar(200) comment '公告内容',
  `create_at` datetime default now() comment '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;