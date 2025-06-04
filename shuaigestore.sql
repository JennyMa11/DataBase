-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: shuaigestore
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `carts` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `food_id` int NOT NULL,
  `quantity` int NOT NULL,
  `total_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`cart_id`),
  KEY `user_id` (`user_id`),
  KEY `food_id` (`food_id`),
  CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`food_id`) REFERENCES `foods` (`food_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
INSERT INTO `carts` VALUES (8,1,1,2,30.00),(9,1,2,1,12.00);
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_cart_total_price` BEFORE UPDATE ON `carts` FOR EACH ROW BEGIN
    -- 更新购物车的总价格
    SET NEW.total_price = NEW.quantity * (SELECT price FROM foods WHERE food_id = NEW.food_id);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `foods`
--

DROP TABLE IF EXISTS `foods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `foods` (
  `food_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `price` decimal(5,2) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`food_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `foods`
--

LOCK TABLES `foods` WRITE;
/*!40000 ALTER TABLE `foods` DISABLE KEYS */;
INSERT INTO `foods` VALUES (1,'汉堡包','经典牛肉汉堡',15.00,NULL),(2,'炸鸡','香脆炸鸡',12.00,NULL),(3,'薯条','金黄薯条',8.00,NULL),(4,'可乐','冰镇可乐',5.00,NULL),(5,'披萨','意式披萨',25.00,NULL),(6,'宫保鸡丁','经典川菜，鸡肉与花生、辣椒炒制而成',20.00,NULL),(7,'麻婆豆腐','麻辣味十足的四川传统豆腐菜',18.00,NULL),(8,'北京烤鸭','经典的北京风味，外脆内嫩',45.00,NULL),(9,'小龙包','鲜美的汤包，经典上海风味',15.00,NULL),(10,'红烧肉','用酱油和糖慢炖的猪肉，色香味俱佳',22.00,NULL),(11,'鱼香肉丝','带有酸、甜、辣味的经典川菜',18.00,NULL),(12,'火锅','辣椒与花椒熬成的汤底，搭配多种食材涮煮',30.00,NULL),(13,'清蒸鲈鱼','鲜嫩的鲈鱼，清蒸保留原味',28.00,NULL),(14,'鱼头豆腐汤','鱼头与豆腐共同熬制，清淡且美味',25.00,NULL),(15,'辣子鸡','鸡肉与干辣椒炒制，辛辣过瘾',20.00,NULL),(16,'口水鸡','鲜美鸡肉浸泡麻辣酱汁，口感独特',18.00,NULL),(17,'西湖醋鱼','西湖的特色，酸甜口味的醋鱼',35.00,NULL),(18,'炸酱面','传统北京小吃，面条与酱料搭配',12.00,NULL),(19,'麻辣小龙虾','麻辣味道浓郁的小龙虾',38.00,NULL),(20,'狮子头','鲜美肉丸，经典的江南菜',24.00,NULL),(21,'涮羊肉','嫩滑羊肉与各种蔬菜一起涮煮',26.00,NULL),(22,'番茄炒蛋','简单的家常菜，酸甜可口',10.00,NULL),(23,'北京炸酱面','北京传统小吃，炸酱拌面',15.00,NULL),(24,'红烧茄子','色香味俱全的红烧茄子',14.00,NULL),(25,'葱烧海参','海参搭配葱烧，营养丰富',50.00,NULL),(26,'food1','美味的food1',444.00,NULL);
/*!40000 ALTER TABLE `foods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `order_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_price` decimal(10,2) NOT NULL,
  `order_status` enum('已完成','制作中','已下单') DEFAULT '已下单',
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,'2025-05-30 08:01:58',268.00,'已下单'),(2,2,'2025-05-30 09:11:55',45.00,'已下单'),(3,2,'2025-05-30 09:11:59',0.00,'已下单'),(4,2,'2025-05-30 09:14:10',67.00,'已下单'),(5,2,'2025-05-30 09:14:14',0.00,'已下单'),(6,2,'2025-05-30 09:14:54',27.00,'已下单'),(7,2,'2025-05-30 09:14:56',0.00,'已下单'),(8,2,'2025-05-30 09:17:21',15.00,'已下单'),(9,2,'2025-05-30 09:17:23',0.00,'已下单'),(10,2,'2025-05-30 09:23:47',30.00,'已下单'),(11,2,'2025-05-30 09:23:48',0.00,'已下单'),(12,2,'2025-05-30 09:24:32',15.00,'已下单'),(13,2,'2025-05-30 09:24:34',0.00,'已下单'),(14,2,'2025-05-30 09:31:07',35.00,'已下单'),(15,2,'2025-05-30 22:27:53',818.00,'已下单');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','scrypt:32768:8:1$7CYeca5YCYzsehNS$dd5712293ae92f037b5a49f1c070ea1d533dcab5b2b5c5266b2a412fe6fd253b845a0f400b326b13ad3f932f7a2b3db073ba69ecce6738c17d84570a15a30ab2','17373604033','admin'),(2,'user','scrypt:32768:8:1$irafHfxMqIoJecf1$d5002bddfaff9939b4113218a13d5480a88775c807b21d80b041a9b630ca425bdce3e3134470deb6e8291dacea437c98e0e99d95cb71eb62a3e3740b71a04f0b','17373604033','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-04 15:45:45
