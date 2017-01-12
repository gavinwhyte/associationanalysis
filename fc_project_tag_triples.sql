/*
 Navicat Premium Data Transfer

 Source Server         : whyteg
 Source Server Type    : PostgreSQL
 Source Server Version : 90601
 Source Host           : localhost
 Source Database       : association
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 90601
 File Encoding         : utf-8

 Date: 01/12/2017 15:11:27 PM
*/

-- ----------------------------
--  Table structure for fc_project_tag_triples
-- ----------------------------
DROP TABLE IF EXISTS "public"."fc_project_tag_triples";
CREATE TABLE "public"."fc_project_tag_triples" (
	"tag1" varchar(255) NOT NULL COLLATE "default",
	"tag2" varchar(255) NOT NULL COLLATE "default",
	"tag3" varchar(255) NOT NULL COLLATE "default",
	"num_projs" int4 NOT NULL
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."fc_project_tag_triples" OWNER TO "whyteg";

