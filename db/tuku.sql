/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50733
 Source Host           : localhost:3306
 Source Schema         : tuku

 Target Server Type    : MySQL
 Target Server Version : 50733
 File Encoding         : 65001

 Date: 16/05/2021 23:08:54
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tuku_admin
-- ----------------------------
DROP TABLE IF EXISTS `tuku_admin`;
CREATE TABLE `tuku_admin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '登录名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '密码',
  `salt` char(6) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '盐值',
  `locked` tinyint(1) NULL DEFAULT 0 COMMENT '禁用(0:否,1:禁用)',
  `role` int(11) NULL DEFAULT 0 COMMENT '角色id',
  `last_time` datetime(0) NULL DEFAULT NULL COMMENT '最近登录时间',
  `create_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tuku_admin
-- ----------------------------
INSERT INTO `tuku_admin` VALUES (1, 'admin123', 'd96256f9a9597a5b945bf7cde2d14e9f16e3c6b57719b5639613736fb2383104', 'ChAETa', 0, 1, '2021-03-01 18:24:12', '2021-04-01 18:02:06');

-- ----------------------------
-- Table structure for tuku_admin_login_history
-- ----------------------------
DROP TABLE IF EXISTS `tuku_admin_login_history`;
CREATE TABLE `tuku_admin_login_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '帐号',
  `ip` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '登录ip',
  `create_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tuku_admin_login_history
-- ----------------------------
INSERT INTO `tuku_admin_login_history` VALUES (1, 'admin123', '192.168.2.103', '2021-04-02 11:04:08');
INSERT INTO `tuku_admin_login_history` VALUES (2, 'admin123', '192.168.2.103', '2021-04-02 11:06:12');
INSERT INTO `tuku_admin_login_history` VALUES (3, 'admin123', '192.168.2.103', '2021-04-02 11:06:27');
INSERT INTO `tuku_admin_login_history` VALUES (4, 'admin123', '192.168.2.103', '2021-04-02 11:06:28');
INSERT INTO `tuku_admin_login_history` VALUES (5, 'admin123', '192.168.2.103', '2021-04-02 11:06:28');
INSERT INTO `tuku_admin_login_history` VALUES (6, 'admin123', '192.168.2.103', '2021-04-02 11:06:28');
INSERT INTO `tuku_admin_login_history` VALUES (7, 'admin123', '192.168.2.103', '2021-04-02 11:06:28');
INSERT INTO `tuku_admin_login_history` VALUES (8, 'admin123', '192.168.2.103', '2021-04-02 11:06:29');
INSERT INTO `tuku_admin_login_history` VALUES (9, 'admin123', '192.168.2.103', '2021-04-02 11:06:41');
INSERT INTO `tuku_admin_login_history` VALUES (10, 'admin123', '192.168.2.103', '2021-04-02 11:18:45');
INSERT INTO `tuku_admin_login_history` VALUES (11, 'admin123', '192.168.2.103', '2021-04-02 11:18:50');
INSERT INTO `tuku_admin_login_history` VALUES (12, 'admin123', '192.168.2.103', '2021-04-02 11:19:24');
INSERT INTO `tuku_admin_login_history` VALUES (13, 'admin123', '192.168.2.103', '2021-04-02 11:20:37');
INSERT INTO `tuku_admin_login_history` VALUES (14, 'admin123', '192.168.2.103', '2021-04-02 11:21:27');
INSERT INTO `tuku_admin_login_history` VALUES (15, 'admin123', '192.168.2.103', '2021-04-02 11:25:30');
INSERT INTO `tuku_admin_login_history` VALUES (16, 'admin123', '192.168.2.103', '2021-04-02 11:26:20');
INSERT INTO `tuku_admin_login_history` VALUES (17, 'admin123', '192.168.2.103', '2021-04-02 11:26:26');
INSERT INTO `tuku_admin_login_history` VALUES (18, 'admin123', '192.168.2.103', '2021-04-02 11:27:30');
INSERT INTO `tuku_admin_login_history` VALUES (19, 'admin123', '192.168.2.103', '2021-04-02 11:27:35');
INSERT INTO `tuku_admin_login_history` VALUES (20, 'admin123', '192.168.2.103', '2021-04-02 11:30:45');
INSERT INTO `tuku_admin_login_history` VALUES (21, 'admin123', '192.168.2.103', '2021-04-02 11:35:24');
INSERT INTO `tuku_admin_login_history` VALUES (22, 'admin123', '::1', '2021-04-02 14:53:54');

-- ----------------------------
-- Table structure for tuku_tie
-- ----------------------------
DROP TABLE IF EXISTS `tuku_tie`;
CREATE TABLE `tuku_tie`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '标题富文本',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '内容富文本',
  `create_at` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tuku_tie
-- ----------------------------
INSERT INTO `tuku_tie` VALUES (1, '<p><span style=\"color: #ff0000;\"><strong><span style=\"color: #ff0000;\">高手帖</span>【021期】<span style=\"color: #00ff00;\">上的飞机阿文u人撒接口返回的是</span></strong></span></p>', '<p><span style=\"color: #ff0000;\"><strong>高手帖【021期】上的<img src=\"https://iknow-pic.cdn.bcebos.com/b151f8198618367a021b7f8b2e738bd4b21ce5d2\" alt=\"d\'s\" width=\"799\" height=\"574\" /></strong></span></p>', '2021-04-01 17:09:13');
INSERT INTO `tuku_tie` VALUES (2, '<p><span style=\"color: #ff0000;\"><strong><span style=\"color: #ff0000;\">高手帖</span>【023期】<span style=\"color: #00ff00;\">上的飞机阿文u人撒接口返回的是</span></strong></span></p>', '<p><span style=\"color: #ff0000;\"><strong>高手帖【021期】上的<img src=\"https://iknow-pic.cdn.bcebos.com/b151f8198618367a021b7f8b2e738bd4b21ce5d2\" alt=\"d\'s\" width=\"799\" height=\"574\" /></strong></span></p>', '2021-04-01 17:09:26');
INSERT INTO `tuku_tie` VALUES (3, '<p><span style=\"color: #ff0000;\"><strong><span style=\"color: #ff0000;\">高手帖</span>【024期】<span style=\"color: #00ff00;\">上的飞机阿文u人撒接口返回的是sdf洒洒水</span></strong></span></p>', '<p><span style=\"color: #ff0000;\"><strong>高手帖【021期】上的<img src=\"https://iknow-pic.cdn.bcebos.com/b151f8198618367a021b7f8b2e738bd4b21ce5d2\" alt=\"d\'s\" width=\"799\" height=\"574\" /></strong></span></p>', '2021-04-01 17:09:28');
INSERT INTO `tuku_tie` VALUES (4, '<p><span style=\"color: #ff0000;\"><strong><span style=\"color: #ff0000;\">高手帖</span>【025期】<span style=\"color: #00ff00;\">上的飞机阿文u人撒接口返回的是</span></strong></span></p>', '<p><span style=\"color: #ff0000;\"><strong>高手帖【021期】上的<img src=\"https://iknow-pic.cdn.bcebos.com/b151f8198618367a021b7f8b2e738bd4b21ce5d2\" alt=\"d\'s\" width=\"799\" height=\"574\" /></strong></span></p>', '2021-04-01 17:09:31');
INSERT INTO `tuku_tie` VALUES (5, '<p>撒范德萨</p>', '<p>萨芬委任为</p>', '2021-04-01 17:09:33');
INSERT INTO `tuku_tie` VALUES (7, '<p><strong><span style=\"text-decoration: underline;\">士大夫</span></strong></p>', '<p><img class=\"wscnph\" src=\"/statics/img/20210402/1617343056205.jpg\" /><img class=\"wscnph\" src=\"http://192.168.2.103:9200 /statics/img/20210402/1617343203682.jpg\" /><img class=\"wscnph\" src=\"http://192.168.2.103:9200/statics/img/20210402/1617343221553.jpg\" /><img class=\"wscnph\" src=\"http://192.168.2.103:9200/statics/img/1617343280042.jpg\" width=\"100\" height=\"200\" /></p>', '2021-04-02 14:01:36');
INSERT INTO `tuku_tie` VALUES (8, '<p><strong><span style=\"text-decoration: underline;\">士大夫</span></strong></p>', '<p><img class=\"wscnph\" src=\"/statics/img/20210402/1617343056205.jpg\" /><img class=\"wscnph\" src=\"http://192.168.2.103:9200 /statics/img/20210402/1617343203682.jpg\" /><img class=\"wscnph\" src=\"http://192.168.2.103:9200/statics/img/20210402/1617343221553.jpg\" /><img class=\"wscnph\" src=\"http://192.168.2.103:9200/statics/img/1617343280042.jpg\" width=\"100\" height=\"200\" /></p>', '2021-04-02 14:01:40');
INSERT INTO `tuku_tie` VALUES (9, '<p>撒<strong><span style=\"color: #ff00ff;\">旦<span style=\"font-size: 12pt;\">发撒打发为</span></span></strong>人<span style=\"font-family: impact, sans-serif;\">踏</span>实的</p>', '<p><span style=\"font-size: 24pt;\">撒旦发顺丰</span></p>\n<p>&nbsp;</p>\n<p><span style=\"font-size: 24pt;\"><img class=\"wscnph\" src=\"http://192.168.2.103:9200/statics/img/1617343698736.jpg\" /></span></p>', '2021-04-02 14:08:26');

SET FOREIGN_KEY_CHECKS = 1;
