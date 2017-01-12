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

 Date: 01/12/2017 15:11:41 PM
*/

-- ----------------------------
--  Table structure for fc_project_tags
-- ----------------------------
DROP TABLE IF EXISTS "public"."fc_project_tags";
CREATE TABLE "public"."fc_project_tags" (
	"project_id" int4 NOT NULL DEFAULT 0,
	"tag_name" varchar(50) NOT NULL DEFAULT '0'::character varying COLLATE "default"
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."fc_project_tags" OWNER TO "whyteg";

-- ----------------------------
--  Primary key structure for table fc_project_tags
-- ----------------------------
ALTER TABLE "public"."fc_project_tags" ADD PRIMARY KEY ("project_id", "tag_name") NOT DEFERRABLE INITIALLY IMMEDIATE;

