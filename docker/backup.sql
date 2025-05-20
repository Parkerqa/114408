-- MySQL dump 10.13  Distrib 8.0.42, for macos15 (arm64)
--
-- Host: 140.131.114.242    Database: 114-408
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.22.04.1

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
-- Table structure for table `accounting`
--

DROP TABLE IF EXISTS `accounting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounting` (
  `accounting_id` int NOT NULL AUTO_INCREMENT,
  `class_info_id` enum('傳統','1') NOT NULL,
  `account_class` varchar(150) DEFAULT NULL,
  `create_id` varchar(150) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `modify_id` varchar(150) DEFAULT NULL,
  `modify_date` datetime(6) DEFAULT NULL,
  `avaible` tinyint NOT NULL,
  PRIMARY KEY (`accounting_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounting`
--

LOCK TABLES `accounting` WRITE;
/*!40000 ALTER TABLE `accounting` DISABLE KEYS */;
INSERT INTO `accounting` VALUES (1,'傳統','12351','1','2004-10-15 00:00:00.000000',NULL,NULL,1),(2,'1','12354684','1','2001-12-22 00:00:00.000000',NULL,NULL,1);
/*!40000 ALTER TABLE `accounting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ai_log`
--

DROP TABLE IF EXISTS `ai_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_log` (
  `ai_id` int NOT NULL AUTO_INCREMENT,
  `log` text NOT NULL,
  `create_id` varchar(150) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  PRIMARY KEY (`ai_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_log`
--

LOCK TABLES `ai_log` WRITE;
/*!40000 ALTER TABLE `ai_log` DISABLE KEYS */;
INSERT INTO `ai_log` VALUES (1,'asdasd','1','2001-10-11 00:00:00.000000');
/*!40000 ALTER TABLE `ai_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_info`
--

DROP TABLE IF EXISTS `class_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_info` (
  `class_id` int NOT NULL AUTO_INCREMENT,
  `money_limit` decimal(10,2) NOT NULL,
  `class_info_id` enum('交通') NOT NULL,
  `create_id` varchar(150) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `modify_id` varchar(150) DEFAULT NULL,
  `modify_date` datetime(6) DEFAULT NULL,
  `available` tinyint NOT NULL,
  PRIMARY KEY (`class_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_info`
--

LOCK TABLES `class_info` WRITE;
/*!40000 ALTER TABLE `class_info` DISABLE KEYS */;
INSERT INTO `class_info` VALUES (2,100000.00,'交通','1','2001-02-11 00:00:00.000000',NULL,NULL,1);
/*!40000 ALTER TABLE `class_info` ENABLE KEYS */;
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
  `red_but` decimal(10,2) NOT NULL,
  `red_top` decimal(10,2) NOT NULL,
  `green_but` decimal(10,2) NOT NULL,
  `green_top` decimal(10,2) NOT NULL,
  `yellow_but` decimal(10,2) NOT NULL,
  `yellow_top` decimal(10,2) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `other_setting`
--

LOCK TABLES `other_setting` WRITE;
/*!40000 ALTER TABLE `other_setting` DISABLE KEYS */;
INSERT INTO `other_setting` VALUES (21,0,0.00,10.00,11.00,70.00,70.00,100.00);
/*!40000 ALTER TABLE `other_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request` (
  `request_id` int NOT NULL,
  `mappping` char(45) NOT NULL,
  `user_agent` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `open_file_path` varchar(255) NOT NULL,
  `http_status_code` char(45) NOT NULL,
  `request_ip_from` varchar(150) NOT NULL,
  `priority` tinyint NOT NULL,
  `request_time` datetime NOT NULL,
  PRIMARY KEY (`request_id`)
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
  `class_info_id` enum('a') DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `check_man` varchar(150) DEFAULT NULL,
  `check_date` datetime(6) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `date` datetime(6) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `create_id` varchar(150) DEFAULT NULL,
  `create_date` datetime(6) DEFAULT NULL,
  `modify_id` varchar(150) DEFAULT NULL,
  `modify_date` datetime(6) DEFAULT NULL,
  `available` tinyint DEFAULT NULL,
  `writeoff_date` datetime(6) DEFAULT NULL,
  `type` enum('電子') DEFAULT NULL,
  `invoice_number` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (24,'a',52,'1','2000-10-11 00:00:00.000000','74bb41972c974fc18bfec6b5264ca630.jpeg',NULL,1,NULL,'2204-09-10 00:00:00.000000','','1999-10-05 00:00:00.000000',1,'2204-09-10 00:00:00.000000','電子','13165153'),(32,'a',58,NULL,'1999-10-05 00:00:00.000000','74bb41972c974fc18bfec6b5264ca630.jpeg',NULL,0,NULL,'2000-10-11 00:00:00.000000',NULL,'1999-10-05 00:00:00.000000',1,'2204-09-10 00:00:00.000000',NULL,NULL),(33,'a',60,NULL,'1234-10-11 00:00:00.000000','39bd00ea4daa4825bbb9b654d310addb.jpeg',NULL,0,NULL,'2000-10-11 00:00:00.000000',NULL,'1999-10-05 00:00:00.000000',1,'2204-09-10 00:00:00.000000',NULL,NULL),(34,'a',62,NULL,'1987-11-04 00:00:00.000000','27dd3e5e311f411db69c9a50d8c42901.jpeg',NULL,2,NULL,'2000-10-11 00:00:00.000000',NULL,'1999-10-05 00:00:00.000000',1,'2204-09-10 00:00:00.000000',NULL,NULL);
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
  `invoice_number` varchar(150) NOT NULL,
  `title` varchar(128) DEFAULT NULL,
  `money` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`td_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_detail`
--

LOCK TABLES `ticket_detail` WRITE;
/*!40000 ALTER TABLE `ticket_detail` DISABLE KEYS */;
INSERT INTO `ticket_detail` VALUES (3,'24','牛肉麵',120.00),(4,'24','綠茶',30.00),(5,'24','牛肉麵',1200.00),(6,'24','綠茶',300.00),(7,'24','牛肉麵',1200.00),(8,'24','綠茶',300.00),(9,'24','牛肉麵',1200.00),(10,'34','綠茶',300.00),(11,'24','牛肉麵',100.00),(12,'1','牛肉麵',1200.00),(13,'1','綠茶',300.00),(14,'1','牛肉麵',1200.00),(15,'1','綠茶',300.00),(16,'1','牛肉麵',NULL);
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
  `create_id` varchar(150) DEFAULT NULL,
  `create_date` datetime(6) DEFAULT NULL,
  `modify_id` varchar(150) DEFAULT NULL,
  `modify_date` datetime(6) DEFAULT NULL,
  `available` tinyint DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'asdsadqw','test.test@test','$2b$12$ljhOGAjEqgleR.VbeMTm1eAqNL4GN4v/7yvKwLTFxScSGF/ycdSka',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,'asdsadqw','test.test@test','$2b$12$KjDvkCr9eLwJtGnYhP032uOR5Y4McCGJItteX6pjk30rMXU12lhKy',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,'asdsadqw','test.test@test','$2b$12$3gRlVoEKATcOP8b661Ai1uqXler6RGb./iU1bUVwe/jZ0zH7nyItW',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,'ashdojsaoidjasd','test@test','$2b$12$n.yulVdGmJfW8huHED/NTe3HdkBL4TKn7FC.9CAqgbD0/mw3bs7IS',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,'example_user','user@example.com','$2b$12$SQbgE2MxUUZ.GT5pnNe/SO69rd7AOlNyl19b41q4BdGef1Gv/mdQO',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,'example_users','user@examplse.com','$2b$12$xM82Q1C43EfmgdPGAgBe2.AfmHd2yPP9gynz.XnQjILVXk9GUKova',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,'example_users','user@examplse.com','$2b$12$9LTtDHUSAYooO.pD3IGhoeTwJGi2i8U/E0sFiQlhVr.IoriFnOIIa',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(8,'example_users','user@examplse.com','$2b$12$Q483JRGComiVDw/21IvNtu20N0r0IznpEJneT6Cvx.PyQ8SMx1O86',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(9,'test','test@etest','$2b$12$hK4QKbjnzzxVAQSuyzGKAeQZ.XiZm6jH/Ut3LvmSe6DLeveAhSBQa',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(10,'test','test@etest','$2b$12$hK4QKbjnzzxVAQSuyzGKAeQZ.XiZm6jH/Ut3LvmSe6DLeveAhSBQa',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(11,'test','testsa@testss','$2b$12$nLpKLe72bTUqBZmmqJkev.DLk0uIZuQDTNA9FMX4XZe4.pX2c6ypC',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(12,'1asd1513632a','testsa@testsss','$2b$12$Fo83NnSPJyZFXRx8vtfRguGIc83UG.4e9fO4HbY9L2BTTsS21dWFO',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(13,'1asd1513632a','testsa@testsss','$2b$12$fZj5BCBz/v7GaUiBa2L9F.un7E.6XYqrXC0XYF4ufWf1oL0W2ePSi',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(14,'1asd1513632as','testsa@testsss','$2b$12$zA5JfP6Jt.HWgMHcb0tOjeq.8d4WiN4CX/Pis4g9PjMSkhqkPOU2a',NULL,NULL,NULL,NULL,NULL,NULL,NULL),(15,'test112','testsadasds@testsss','$2b$12$jKXa55QfnmleLfvK1ldpOuMAqW.VZ0kO3vs7/Odq7yllLy0TyeKiG',0,NULL,NULL,NULL,NULL,NULL,NULL),(16,'test112','testsadasds@testsss','$2b$12$ibkwt9.Y3Zh1Y1w79gk4q.5TrO9YhMsLGis2StJCtBxmdE/udXuoG',0,NULL,NULL,NULL,NULL,NULL,NULL),(17,'test111','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL,NULL,NULL,NULL,NULL,NULL),(18,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL,NULL,NULL,NULL,NULL,NULL),(19,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL,NULL,NULL,NULL,NULL,NULL),(20,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL,NULL,NULL,NULL,NULL,NULL),(21,'test11144','tsdasds@t','$2b$12$RuwOGuyWCZnwN2Z.CYfY8eAlaArcbPQX2JHz3U6DCdcVTzjNPoEoi',0,'ad46bb98087847bca22113dc8b11830b.png',NULL,NULL,NULL,NULL,NULL),(44,'test0425','test0425@gmail.com','$2b$12$Mj0QTzAQFn/l4k/mtEz0UOtDwQZ/Cl7lneVzz.EMLyGOiyCHi1gey',0,NULL,NULL,NULL,NULL,NULL,NULL),(45,'test0425','test0425@gmail.com','$2b$12$U6VRXXNmLrnfFn.9CDo4h.mi0pSdIGNrgDyaw9bbaT6UWOlBmzy9a',0,NULL,NULL,NULL,NULL,NULL,NULL),(46,'test0425','test0425@gmail.com','$2b$12$DQ3oxnTZgSryLpWLLzjTpesXaeAtBtkFSsTk3U9cNo13v0QfOc7Si',0,NULL,NULL,NULL,NULL,NULL,NULL),(47,'test0425','test0425@gmail.com','$2b$12$7RlyUE0GjVe/bbFEnTI80OjQixiBZhhGJ76fMFfVauj0BxL5H9rKS',0,NULL,NULL,NULL,NULL,NULL,NULL),(48,'test0425','test0425@gmail.com','$2b$12$/FR5wB5Ql4QHUwojgQmqaO.wRTFDdY6FPFAY2NW.WA0utFku/t/d6',0,NULL,NULL,NULL,NULL,NULL,NULL),(49,'test0425','test0425@gmail.com','$2b$12$yRBz7EfSEMsDY0O73bAOWu17a6oTpSJav8BlbjRsruVyIMDTXgTF2',0,NULL,NULL,NULL,NULL,NULL,NULL),(50,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL,NULL,NULL,NULL,NULL,NULL),(51,'asadqwe','tsdassssds@tassssss','$2b$12$/VKD/wCubi6oK9aBtbPJq.ODdmhA8oheeY6Tf3NQsfFxSI1/YSCXa',0,NULL,NULL,NULL,NULL,NULL,NULL),(52,'testuser','testuser@gmail.com','$2b$12$.MMMu/Ih0laMcf1Vjis1O.beIuhTyZI/2b2q9A2rjjC4xrj1UR0b2',0,NULL,NULL,NULL,NULL,NULL,NULL),(53,'test111441','tsdasds@ta','$2b$12$j2DT8ts.8lUZyxALCMukvO.syo5cfOxYQiCMQ2HNkb1teIUz9Q.cK',0,NULL,NULL,NULL,NULL,NULL,NULL),(54,'test11144ssssss','tsdassssds@tassssss','$2b$12$cuDnCg5X/VoXdu49cLoXK.FuiTIzMbnVp7I3uaLvUjIGQJDPLmjH6',0,NULL,NULL,NULL,NULL,NULL,NULL),(55,'test1114412222','asdsadsadsadasda@asdasdassd','$2b$12$fZ52Vqw41BlrytmO/e6ZyeFkzTSnW8JggIJ2oic7Tcse2n.F7c8oq',0,NULL,NULL,NULL,NULL,NULL,NULL),(56,'烤焦ss','asdjioasd@jassd','$2b$12$XEryqa6wPDzx2FJFIBKOz.tl4nAbh3S66l3ULbVRG2DEy0z3pDiQ2',0,NULL,NULL,NULL,NULL,NULL,NULL),(57,'0429','0429@gmail.com','$2b$12$mBDegYXqfZcdLyEoeXij6Ors0jr5M1T3W3a/kBL4bNCN8BRsvZ7la',0,NULL,NULL,NULL,NULL,NULL,NULL),(58,'烤焦ss','asdddjioasd@jassd','$2b$12$6u0ya590JsPFL6e1DvdNuOecppsLbJkr4TkMwFJ9abNlKlxrlnl2u',0,'f1c19d64ffbe47199b007c6366a057e7.jpeg',NULL,NULL,NULL,NULL,NULL),(59,'test11144122222','tsdassssdss@ta','$2b$12$G3n6bMTSZPron.zDrgerFOjz4p23Q4/ocZtgdE73ObvSGCc0d0/wO',0,NULL,NULL,NULL,NULL,NULL,NULL),(60,'test1114412222ss2','tsdassssdss@tass','$2b$12$sEpM0O0lESTHIG8RAm7NvurukJAC6ZXEaoxVMCaw6VQDwdZRnj9Sq',1,'f40c265d7b8148229a0ead836f6f810c.jpeg',NULL,NULL,NULL,NULL,NULL),(61,'好A','aaa@gmail.com','$2b$12$632BLX3afs3cmux35.LA0e2y392frDtPEecL.EFOnS9HFrCANI1/u',0,NULL,NULL,NULL,NULL,NULL,NULL),(62,'烤焦ss','asdddjioasd@jassd','$2b$12$04HzPMmkCeFSc5j06Yg5Ke9naKyIyBgFeZN7JDQSnBwrEpU.yEGIS',0,'a6dc9c010b024263bc5c4bd695c91289.jpeg',NULL,NULL,NULL,NULL,NULL),(63,'烤焦ss','asdddjioasd@jassd','$2b$12$54ouMRSbsDt57.YM3JnY5Og3L6hAecXODCwpddbZ77hl5t0Acd/Qe',1,NULL,NULL,NULL,NULL,NULL,NULL),(64,'test1114412222ss2s','tsdasssssdss@tassss','$2b$12$m7p823BO7VtSMG.ixQCgH.8TEvr2tcyiz01/5qN3h5UmrC0bqVnau',0,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database '114-408'
--

--
-- Dumping routines for database '114-408'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-13 15:36:30
