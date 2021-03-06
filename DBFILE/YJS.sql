-- MySQL Script generated by MySQL Workbench
-- Thu Jul 20 09:39:59 2017
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema spider
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema spider
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `spider` DEFAULT CHARACTER SET utf8 ;
USE `spider` ;

-- -----------------------------------------------------
-- Table `spider`.`yjs_other`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `spider`.`yjs_other` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(255) NULL COMMENT '页面链接',
  `url_md5` VARCHAR(100) NULL COMMENT 'URL地址md5',
  `title` VARCHAR(300) NULL COMMENT '列表页标题',
  `tag` VARCHAR(45) NULL COMMENT '列表页信息来源',
  `company` VARCHAR(255) NULL COMMENT '公司名',
  `post_date` VARCHAR(25) NULL COMMENT '发布时间',
  `location` VARCHAR(255) NULL COMMENT '工作地点',
  `position_title` VARCHAR(255) NULL COMMENT '职位名称',
  `position_type` VARCHAR(45) NULL COMMENT '职位类型',
  `source` VARCHAR(45) NULL COMMENT '详情页来源',
  `major_label` VARCHAR(255) NULL COMMENT '专业标签',
  `content` LONGTEXT NULL COMMENT '正文',
  `created_at` INT(11) NULL COMMENT '创建时间',
  `position` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = '应届生招聘网站上非自身网站的数据';


-- -----------------------------------------------------
-- Table `spider`.`yjs_self`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `spider`.`yjs_self` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(255) NULL COMMENT '页面链接',
  `url_md5` VARCHAR(100) NULL COMMENT 'Url 的 md5',
  `title` VARCHAR(300) NULL COMMENT '标题',
  `tag` VARCHAR(45) NULL COMMENT '列表页信息来源',
  `company` VARCHAR(255) NULL COMMENT '企业名称',
  `industry` VARCHAR(45) NULL COMMENT '所属行业',
  `company_size` VARCHAR(45) NULL COMMENT '企业规模',
  `company_type` VARCHAR(45) NULL COMMENT '企业性质',
  `position_title` VARCHAR(100) NULL COMMENT '职位名称',
  `location` VARCHAR(45) NULL COMMENT '工作地点',
  `recruit_num` VARCHAR(45) NULL COMMENT '招聘人数',
  `position_type` VARCHAR(45) NULL COMMENT '职位性质',
  `position_desc` LONGTEXT NULL COMMENT '职位描述',
  `company_intro` LONGTEXT NULL COMMENT '企业简介',
  `company_site` VARCHAR(255) NULL COMMENT '企业网站',
  `created_at` INT(11) NULL COMMENT '创建时间',
  `valid_date` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COMMENT = '应届生网站上自身网站的数据'
PACK_KEYS = Default;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
