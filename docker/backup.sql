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
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `uid` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(100) NOT NULL,
  `priority` int DEFAULT NULL,
  `img` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'asdsadqw','test.test@test','$2b$12$ljhOGAjEqgleR.VbeMTm1eAqNL4GN4v/7yvKwLTFxScSGF/ycdSka',NULL,NULL),(2,'asdsadqw','test.test@test','$2b$12$KjDvkCr9eLwJtGnYhP032uOR5Y4McCGJItteX6pjk30rMXU12lhKy',NULL,NULL),(3,'asdsadqw','test.test@test','$2b$12$3gRlVoEKATcOP8b661Ai1uqXler6RGb./iU1bUVwe/jZ0zH7nyItW',NULL,NULL),(4,'ashdojsaoidjasd','test@test','$2b$12$n.yulVdGmJfW8huHED/NTe3HdkBL4TKn7FC.9CAqgbD0/mw3bs7IS',NULL,NULL),(5,'example_user','user@example.com','$2b$12$SQbgE2MxUUZ.GT5pnNe/SO69rd7AOlNyl19b41q4BdGef1Gv/mdQO',NULL,NULL),(6,'example_users','user@examplse.com','$2b$12$xM82Q1C43EfmgdPGAgBe2.AfmHd2yPP9gynz.XnQjILVXk9GUKova',NULL,NULL),(7,'example_users','user@examplse.com','$2b$12$9LTtDHUSAYooO.pD3IGhoeTwJGi2i8U/E0sFiQlhVr.IoriFnOIIa',NULL,NULL),(8,'example_users','user@examplse.com','$2b$12$Q483JRGComiVDw/21IvNtu20N0r0IznpEJneT6Cvx.PyQ8SMx1O86',NULL,NULL),(9,'test','test@etest','$2b$12$hK4QKbjnzzxVAQSuyzGKAeQZ.XiZm6jH/Ut3LvmSe6DLeveAhSBQa',NULL,NULL),(10,'test','test@etest','$2b$12$hK4QKbjnzzxVAQSuyzGKAeQZ.XiZm6jH/Ut3LvmSe6DLeveAhSBQa',NULL,NULL),(11,'test','testsa@testss','$2b$12$nLpKLe72bTUqBZmmqJkev.DLk0uIZuQDTNA9FMX4XZe4.pX2c6ypC',NULL,NULL),(12,'1asd1513632a','testsa@testsss','$2b$12$Fo83NnSPJyZFXRx8vtfRguGIc83UG.4e9fO4HbY9L2BTTsS21dWFO',NULL,NULL),(13,'1asd1513632a','testsa@testsss','$2b$12$fZj5BCBz/v7GaUiBa2L9F.un7E.6XYqrXC0XYF4ufWf1oL0W2ePSi',NULL,NULL),(14,'1asd1513632as','testsa@testsss','$2b$12$zA5JfP6Jt.HWgMHcb0tOjeq.8d4WiN4CX/Pis4g9PjMSkhqkPOU2a',NULL,NULL),(15,'test112','testsadasds@testsss','$2b$12$jKXa55QfnmleLfvK1ldpOuMAqW.VZ0kO3vs7/Odq7yllLy0TyeKiG',0,NULL),(16,'test112','testsadasds@testsss','$2b$12$ibkwt9.Y3Zh1Y1w79gk4q.5TrO9YhMsLGis2StJCtBxmdE/udXuoG',0,NULL),(17,'test111','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL),(18,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL),(19,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL),(20,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL),(21,'test11144','tsdasds@t','$2b$12$RuwOGuyWCZnwN2Z.CYfY8eAlaArcbPQX2JHz3U6DCdcVTzjNPoEoi',0,'ad46bb98087847bca22113dc8b11830b.png'),(44,'test0425','test0425@gmail.com','$2b$12$Mj0QTzAQFn/l4k/mtEz0UOtDwQZ/Cl7lneVzz.EMLyGOiyCHi1gey',0,NULL),(45,'test0425','test0425@gmail.com','$2b$12$U6VRXXNmLrnfFn.9CDo4h.mi0pSdIGNrgDyaw9bbaT6UWOlBmzy9a',0,NULL),(46,'test0425','test0425@gmail.com','$2b$12$DQ3oxnTZgSryLpWLLzjTpesXaeAtBtkFSsTk3U9cNo13v0QfOc7Si',0,NULL),(47,'test0425','test0425@gmail.com','$2b$12$7RlyUE0GjVe/bbFEnTI80OjQixiBZhhGJ76fMFfVauj0BxL5H9rKS',0,NULL),(48,'test0425','test0425@gmail.com','$2b$12$/FR5wB5Ql4QHUwojgQmqaO.wRTFDdY6FPFAY2NW.WA0utFku/t/d6',0,NULL),(49,'test0425','test0425@gmail.com','$2b$12$yRBz7EfSEMsDY0O73bAOWu17a6oTpSJav8BlbjRsruVyIMDTXgTF2',0,NULL),(50,'test11144','tsestsadasds@testsss','$2b$12$EDinmkn4qYlCvCj1ixyN0Ov3F.07engJVfquDDOTULoY238A9iwDy',0,NULL),(51,'asadqwe','tsdassssds@tassssss','$2b$12$/VKD/wCubi6oK9aBtbPJq.ODdmhA8oheeY6Tf3NQsfFxSI1/YSCXa',0,NULL),(52,'testuser','testuser@gmail.com','$2b$12$.MMMu/Ih0laMcf1Vjis1O.beIuhTyZI/2b2q9A2rjjC4xrj1UR0b2',0,NULL),(53,'test111441','tsdasds@ta','$2b$12$j2DT8ts.8lUZyxALCMukvO.syo5cfOxYQiCMQ2HNkb1teIUz9Q.cK',0,NULL),(54,'test11144ssssss','tsdassssds@tassssss','$2b$12$cuDnCg5X/VoXdu49cLoXK.FuiTIzMbnVp7I3uaLvUjIGQJDPLmjH6',0,NULL),(55,'test1114412222','asdsadsadsadasda@asdasdassd','$2b$12$fZ52Vqw41BlrytmO/e6ZyeFkzTSnW8JggIJ2oic7Tcse2n.F7c8oq',0,NULL),(56,'烤焦ss','asdjioasd@jassd','$2b$12$XEryqa6wPDzx2FJFIBKOz.tl4nAbh3S66l3ULbVRG2DEy0z3pDiQ2',0,NULL),(57,'0429','0429@gmail.com','$2b$12$mBDegYXqfZcdLyEoeXij6Ors0jr5M1T3W3a/kBL4bNCN8BRsvZ7la',0,NULL),(58,'烤焦ss','asdddjioasd@jassd','$2b$12$6u0ya590JsPFL6e1DvdNuOecppsLbJkr4TkMwFJ9abNlKlxrlnl2u',0,'f1c19d64ffbe47199b007c6366a057e7.jpeg'),(59,'test11144122222','tsdassssdss@ta','$2b$12$G3n6bMTSZPron.zDrgerFOjz4p23Q4/ocZtgdE73ObvSGCc0d0/wO',0,NULL),(60,'test1114412222ss2','tsdassssdss@tass','$2b$12$sEpM0O0lESTHIG8RAm7NvurukJAC6ZXEaoxVMCaw6VQDwdZRnj9Sq',1,'f40c265d7b8148229a0ead836f6f810c.jpeg'),(61,'好A','aaa@gmail.com','$2b$12$632BLX3afs3cmux35.LA0e2y392frDtPEecL.EFOnS9HFrCANI1/u',0,NULL),(62,'烤焦ss','asdddjioasd@jassd','$2b$12$04HzPMmkCeFSc5j06Yg5Ke9naKyIyBgFeZN7JDQSnBwrEpU.yEGIS',0,'a6dc9c010b024263bc5c4bd695c91289.jpeg'),(63,'烤焦ss','asdddjioasd@jassd','$2b$12$54ouMRSbsDt57.YM3JnY5Og3L6hAecXODCwpddbZ77hl5t0Acd/Qe',1,NULL),(64,'test1114412222ss2s','tsdasssssdss@tassss','$2b$12$m7p823BO7VtSMG.ixQCgH.8TEvr2tcyiz01/5qN3h5UmrC0bqVnau',0,NULL);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounting`
--

DROP TABLE IF EXISTS `accounting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounting` (
  `acid` int NOT NULL AUTO_INCREMENT,
  `class` varchar(45) DEFAULT NULL,
  `account_class` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`acid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounting`
--

LOCK TABLES `accounting` WRITE;
/*!40000 ALTER TABLE `accounting` DISABLE KEYS */;
INSERT INTO `accounting` VALUES (1,'傳統','12351'),(2,'1','12354684');
/*!40000 ALTER TABLE `accounting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `class_info`
--

DROP TABLE IF EXISTS `class_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_info` (
  `cid` int NOT NULL AUTO_INCREMENT,
  `money_limit` varchar(45) DEFAULT NULL,
  `class` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_info`
--

LOCK TABLES `class_info` WRITE;
/*!40000 ALTER TABLE `class_info` DISABLE KEYS */;
INSERT INTO `class_info` VALUES (2,'100000','交通');
/*!40000 ALTER TABLE `class_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `other_setting`
--

DROP TABLE IF EXISTS `other_setting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `other_setting` (
  `uid` int NOT NULL,
  `theme` int DEFAULT NULL,
  `red_but` int DEFAULT NULL,
  `red_top` int DEFAULT NULL,
  `green_but` int DEFAULT NULL,
  `green_top` int DEFAULT NULL,
  `yellow_but` int DEFAULT NULL,
  `yellow_top` int DEFAULT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `other_setting`
--

LOCK TABLES `other_setting` WRITE;
/*!40000 ALTER TABLE `other_setting` DISABLE KEYS */;
INSERT INTO `other_setting` VALUES (21,0,NULL,NULL,NULL,NULL,NULL,NULL),(51,0,NULL,NULL,NULL,NULL,NULL,NULL),(58,0,NULL,NULL,NULL,NULL,NULL,NULL),(60,0,NULL,NULL,NULL,NULL,NULL,NULL),(62,0,NULL,NULL,NULL,NULL,NULL,NULL),(64,NULL,0,30,61,100,31,60);
/*!40000 ALTER TABLE `other_setting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket`
--

DROP TABLE IF EXISTS `ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ticket` (
  `tid` int NOT NULL AUTO_INCREMENT,
  `class` varchar(45) DEFAULT NULL,
  `uid` int DEFAULT NULL,
  `check_man` varchar(45) DEFAULT NULL,
  `check_date` varchar(45) DEFAULT NULL,
  `img` varchar(45) DEFAULT NULL,
  `status` int DEFAULT NULL,
  `creatid` varchar(45) DEFAULT NULL,
  `creatdate` date DEFAULT NULL,
  `modifyid` varchar(45) DEFAULT NULL,
  `modifydate` varchar(45) DEFAULT NULL,
  `available` varchar(45) DEFAULT NULL,
  `writeoff_date` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `invoice_number` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`tid`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket`
--

LOCK TABLES `ticket` WRITE;
/*!40000 ALTER TABLE `ticket` DISABLE KEYS */;
INSERT INTO `ticket` VALUES (1,'傳統',60,'1','1','',1,'','2004-12-22','','','','1','1','asjdioasjiodjasd'),(24,'a',52,'1','1','',1,NULL,'2204-09-10','','','','1','1','13165153'),(25,'aa',52,'1','1','',1,'','2204-10-10','','','','1','1','12..12.4545'),(26,'eas',52,'1','11','',0,'','2204-12-10','','','','1','1','454212785'),(27,'adw',52,'11','1','',1,'','2504-12-10','',NULL,NULL,'1','1','12345368'),(28,'ss',52,'1','1','',1,'','2304-12-10','',NULL,NULL,'1','1','142312354312'),(29,'bc',52,'1','1','',1,'','2004-12-10','',NULL,NULL,'1','1','5431237531'),(30,'ssdasd',52,'1','1','af8935976c8e43c69a01b28f109c33dd.jpeg',1,'','2214-12-10',NULL,NULL,NULL,'1','1','453123453123'),(31,'asdsad',52,'1','1','baff9cd0f0ae40d38b28773711eee939.png',1,'','2214-10-10',NULL,NULL,NULL,'2004-12-11','1','45312374853'),(32,NULL,58,NULL,NULL,'74bb41972c974fc18bfec6b5264ca630.jpeg',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(33,NULL,60,NULL,NULL,'39bd00ea4daa4825bbb9b654d310addb.jpeg',0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(34,NULL,62,NULL,NULL,'27dd3e5e311f411db69c9a50d8c42901.jpeg',2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
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
  `tid` varchar(45) DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `money` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`td_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_detail`
--

LOCK TABLES `ticket_detail` WRITE;
/*!40000 ALTER TABLE `ticket_detail` DISABLE KEYS */;
INSERT INTO `ticket_detail` VALUES (3,'24','牛肉麵','120'),(4,'24','綠茶','30'),(5,'24','牛肉麵','1200'),(6,'24','綠茶','300'),(7,'24','牛肉麵','1200'),(8,'24','綠茶','300'),(9,'24','牛肉麵','1200'),(10,'34','綠茶','300'),(11,'24','牛肉麵','100'),(12,'1','牛肉麵','1200'),(13,'1','綠茶','300'),(14,'1','牛肉麵','1200'),(15,'1','綠茶','300'),(16,'1','牛肉麵',NULL);
/*!40000 ALTER TABLE `ticket_detail` ENABLE KEYS */;
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

-- Dump completed on 2025-05-08  8:22:32
