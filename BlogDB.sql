/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : BlogDB

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 05/01/2019 22:51:58
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ssp_article
-- ----------------------------
DROP TABLE IF EXISTS `ssp_article`;
CREATE TABLE `ssp_article`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '标题',
  `author_id` int(11) NOT NULL COMMENT '作者编号',
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '作者名称',
  `released_at` bigint(255) NOT NULL COMMENT '发布时间',
  `promote_intro` varchar(500) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `tag_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '分类',
  `tag_title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `likes_count` int(255) NULL DEFAULT NULL COMMENT '点赞',
  `comments_count` int(255) NULL DEFAULT NULL COMMENT '评论数',
  `keywords` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '关键词',
  `content` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL COMMENT '内容',
  `banner` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL,
  `article_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_article_id`(`article_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1587 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ssp_author
-- ----------------------------
DROP TABLE IF EXISTS `ssp_author`;
CREATE TABLE `ssp_author`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '头像',
  `bio` varchar(1000) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '简介',
  `liked_count` int(255) NULL DEFAULT NULL COMMENT '获赞数',
  `all_words_count` int(255) NULL DEFAULT NULL COMMENT '写作总字数',
  `attention_count` int(255) NULL DEFAULT NULL COMMENT '关注总数\r\n',
  `followed_count` int(255) NULL DEFAULT NULL COMMENT '粉丝数量',
  `author_id` int(11) NULL DEFAULT NULL COMMENT '作者编号',
  `articles_count` int(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_author_id`(`author_id`) USING BTREE COMMENT '作者编号唯一索引'
) ENGINE = InnoDB AUTO_INCREMENT = 1572 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ssp_comments
-- ----------------------------
DROP TABLE IF EXISTS `ssp_comments`;
CREATE TABLE `ssp_comments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comments` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL COMMENT '评论',
  `released_at` bigint(255) NULL DEFAULT NULL,
  `pick_count` int(255) NULL DEFAULT NULL COMMENT '点赞数',
  `tread_count` int(255) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `comment_id` int(11) NULL DEFAULT NULL COMMENT '评论编号（回复评论标志）',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16989 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ssp_dictionary
-- ----------------------------
DROP TABLE IF EXISTS `ssp_dictionary`;
CREATE TABLE `ssp_dictionary`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '标题',
  `kind` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT NULL COMMENT '类型 0tag 1 topics',
  `_id` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_id_kind`(`kind`, `_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3635 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
