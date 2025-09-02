CREATE DATABASE  IF NOT EXISTS `114408` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `114408`;
-- MySQL dump 10.13  Distrib 8.0.42, for macos15 (arm64)
--
-- Host: 127.0.0.1    Database: 114408
-- ------------------------------------------------------
-- Server version	8.4.4

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounting_items`
--

DROP TABLE IF EXISTS `accounting_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounting_items` (
  `accounting_id` bigint NOT NULL AUTO_INCREMENT,
  `account_code` varchar(50) NOT NULL,
  `account_name` varchar(150) NOT NULL,
  `account_class` varchar(150) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(150) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`accounting_id`),
  UNIQUE KEY `uk_accounting_code` (`account_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounting_items`
--

LOCK TABLES `accounting_items` WRITE;
/*!40000 ALTER TABLE `accounting_items` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounting_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ai_log`
--

DROP TABLE IF EXISTS `ai_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_log` (
  `ai_id` int NOT NULL AUTO_INCREMENT,
  `prompt` text NOT NULL,
  `log` text NOT NULL,
  `created_by` varchar(150) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`ai_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_log`
--

LOCK TABLES `ai_log` WRITE;
/*!40000 ALTER TABLE `ai_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `ai_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department_accounting`
--

DROP TABLE IF EXISTS `department_accounting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department_accounting` (
  `dept_accounting_id` bigint NOT NULL AUTO_INCREMENT,
  `department_id` bigint NOT NULL,
  `accounting_id` bigint NOT NULL,
  `budget_limit` decimal(12,2) NOT NULL DEFAULT '0.00',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(150) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`dept_accounting_id`),
  UNIQUE KEY `uk_da` (`department_id`,`accounting_id`),
  KEY `fk_da_accounting` (`accounting_id`),
  CONSTRAINT `fk_da_accounting` FOREIGN KEY (`accounting_id`) REFERENCES `accounting_items` (`accounting_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_da_department` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department_accounting`
--

LOCK TABLES `department_accounting` WRITE;
/*!40000 ALTER TABLE `department_accounting` DISABLE KEYS */;
/*!40000 ALTER TABLE `department_accounting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` bigint NOT NULL AUTO_INCREMENT,
  `dept_code` varchar(50) NOT NULL,
  `dept_name` varchar(150) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` varchar(150) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_by` varchar(150) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`department_id`),
  UNIQUE KEY `uk_departments_code` (`dept_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `other_setting`
--

DROP TABLE IF EXISTS `other_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `other_setting` (
  `user_id` int NOT NULL,
  `theme` int NOT NULL,
  `red_bot` decimal(10,2) NOT NULL,
  `red_top` decimal(10,2) NOT NULL,
  `green_bot` decimal(10,2) NOT NULL,
  `green_top` decimal(10,2) NOT NULL,
  `yellow_bot` decimal(10,2) NOT NULL,
  `yellow_top` decimal(10,2) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `other_setting`
--

LOCK TABLES `other_setting` WRITE;
/*!40000 ALTER TABLE `other_setting` DISABLE KEYS */;
INSERT INTO `other_setting` VALUES (1,0,0.00,50.00,51.00,70.00,71.00,100.00);
/*!40000 ALTER TABLE `other_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `mappping` char(45) NOT NULL,
  `user_agent` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `open_file_path` varchar(255) NOT NULL,
  `http_status_code` char(45) NOT NULL,
  `request_ip_from` varchar(150) NOT NULL,
  `priority` tinyint NOT NULL,
  `request_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `ticket_id` int NOT NULL AUTO_INCREMENT,
  `type` int DEFAULT NULL,
  `invoice_number` varchar(10) DEFAULT NULL,
  `class_info_id` enum('a') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `check_man` varchar(150) DEFAULT NULL,
  `check_date` datetime DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `total_money` decimal(10,2) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `writeoff_date` datetime DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` varchar(150) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_by` varchar(150) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_detail`
--

DROP TABLE IF EXISTS `ticket_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket_detail` (
  `td_id` int NOT NULL AUTO_INCREMENT,
  `ticket_id` int NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `money` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`td_id`),
  KEY `fk_ticket_detail_ticket` (`ticket_id`),
  CONSTRAINT `fk_ticket_detail_ticket` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_detail`
--

LOCK TABLES `ticket_detail` WRITE;
/*!40000 ALTER TABLE `ticket_detail` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(150) DEFAULT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `priority` int DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_by` varchar(150) NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_by` varchar(150) DEFAULT NULL,
  `updated_at` datetime(6) DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'user','user@example.com','$2b$12$l3bU0Xt8hwIQ6j8IszI.9OvqewE0znCsbSn.zB6QLDKJXjLPvx.rC',0,'user.png',1,'','2025-09-02 09:17:49.025654',NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database '114408'
--

--
-- Dumping routines for database '114408'
--
/*!50003 DROP PROCEDURE IF EXISTS `ensure_audit_columns` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `ensure_audit_columns`(IN in_schema VARCHAR(64), IN in_table VARCHAR(64))
BEGIN
  DECLARE col_exists INT;

  -- is_active
  SELECT COUNT(*) INTO col_exists FROM information_schema.columns
   WHERE table_schema = in_schema AND table_name = in_table AND column_name = 'is_active';
  IF col_exists = 0 THEN
    SET @sql = CONCAT('ALTER TABLE `', in_schema, '`.`', in_table, '` ',
                      'ADD COLUMN is_active TINYINT(1) NOT NULL DEFAULT 1');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
  END IF;

  -- created_by
  SELECT COUNT(*) INTO col_exists FROM information_schema.columns
   WHERE table_schema = in_schema AND table_name = in_table AND column_name = 'created_by';
  IF col_exists = 0 THEN
    SET @sql = CONCAT('ALTER TABLE `', in_schema, '`.`', in_table, '` ',
                      'ADD COLUMN created_by VARCHAR(150) NOT NULL');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
  END IF;

  -- created_at
  SELECT COUNT(*) INTO col_exists FROM information_schema.columns
   WHERE table_schema = in_schema AND table_name = in_table AND column_name = 'created_at';
  IF col_exists = 0 THEN
    SET @sql = CONCAT('ALTER TABLE `', in_schema, '`.`', in_table, '` ',
                      'ADD COLUMN created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
  END IF;

  -- updated_by
  SELECT COUNT(*) INTO col_exists FROM information_schema.columns
   WHERE table_schema = in_schema AND table_name = in_table AND column_name = 'updated_by';
  IF col_exists = 0 THEN
    SET @sql = CONCAT('ALTER TABLE `', in_schema, '`.`', in_table, '` ',
                      'ADD COLUMN updated_by VARCHAR(150) NULL');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
  END IF;

  -- updated_at
  SELECT COUNT(*) INTO col_exists FROM information_schema.columns
   WHERE table_schema = in_schema AND table_name = in_table AND column_name = 'updated_at';
  IF col_exists = 0 THEN
    SET @sql = CONCAT('ALTER TABLE `', in_schema, '`.`', in_table, '` ',
                      'ADD COLUMN updated_at DATETIME(6) NULL ON UPDATE CURRENT_TIMESTAMP(6)');
    PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;
  END IF;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-02 17:29:29
