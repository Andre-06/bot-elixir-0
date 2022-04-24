CREATE DATABASE  IF NOT EXISTS `elixirdatabase` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `elixirdatabase`;
-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: elixirdatabase
-- ------------------------------------------------------
-- Server version	5.7.31

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
-- Table structure for table `armas`
--

DROP TABLE IF EXISTS `armas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `armas` (
  `idarmas` int(11) NOT NULL AUTO_INCREMENT,
  `idpersonagem` int(11) DEFAULT NULL,
  `item` varchar(50) DEFAULT NULL,
  `peso` decimal(4,2) DEFAULT NULL,
  `dano` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`idarmas`),
  KEY `idpersonagem` (`idpersonagem`)
) ENGINE=MyISAM AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `armas`
--

LOCK TABLES `armas` WRITE;
/*!40000 ALTER TABLE `armas` DISABLE KEYS */;
INSERT INTO `armas` VALUES (1,4,'Adaga ',0.50,'1d4 '),(2,4,'Arco Médio ',2.00,'1d4 '),(3,6,'martelo de guerra ',10.00,'1d10+5 '),(4,6,'2 machado médio ',4.00,'1d8+5 '),(5,8,'mangual reliquea ',4.00,'0 '),(6,8,'forma 1 mangual(f1) ',0.00,'1d12+5 '),(7,8,'forma 3 mangual(f3) ',0.00,'2d6+5 '),(8,8,'forma 5 mangual(f5) ',0.00,'2d8+5 '),(9,8,'forma 7 mangual(f7) ',0.00,'1d10+5 '),(10,8,'forma 8 mangual(f8) ',0.00,'2d12+5 '),(11,8,'forma 9 mangual(f9) ',0.00,'2d20+5 '),(12,10,'foice dupla ',2.00,'1d8+STR '),(13,13,'garras ',1.00,'1d8+STR '),(14,18,'arminha toop ',55.00,'1d99999 '),(15,18,'2 Tekko Kagi ',2.00,'1d4 '),(16,20,'adaga ',1.00,'1d4+DEX '),(17,20,'espada ',3.00,'1d6+STR '),(18,20,'picareta ',5.00,'1d10+STR '),(50,20,'soco ingles',1.00,'2d4+STR'),(20,21,'Espada Gótica ',2.00,'1d8+5 '),(21,21,'Espada do Jorge ',2.00,'1d6+5 '),(32,5,'lança',2.00,'1d6+DEX'),(29,13,'espada',2.00,'1d6+STR'),(31,5,'adaga',1.00,'1d4+STR'),(33,5,'cutelo',1.00,'1d4+STR'),(49,34,' espada',4.00,'1d6'),(48,34,' foice',5.00,'1d4');
/*!40000 ALTER TABLE `armas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `atributos`
--

DROP TABLE IF EXISTS `atributos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `atributos` (
  `idatributos` int(11) NOT NULL AUTO_INCREMENT,
  `personagematributos` varchar(30) DEFAULT NULL,
  `str` tinyint(4) DEFAULT NULL,
  `modstr` tinyint(4) DEFAULT NULL,
  `dex` tinyint(4) DEFAULT NULL,
  `moddex` tinyint(4) DEFAULT NULL,
  `con` tinyint(4) DEFAULT NULL,
  `modcon` tinyint(4) DEFAULT NULL,
  `inte` tinyint(4) DEFAULT NULL,
  `modinte` tinyint(4) DEFAULT NULL,
  `wis` tinyint(4) DEFAULT NULL,
  `modwis` tinyint(4) DEFAULT NULL,
  `cha` tinyint(4) DEFAULT NULL,
  `modcha` tinyint(4) DEFAULT NULL,
  `pod` tinyint(4) DEFAULT NULL,
  `modpod` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`idatributos`)
) ENGINE=MyISAM AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `atributos`
--

LOCK TABLES `atributos` WRITE;
/*!40000 ALTER TABLE `atributos` DISABLE KEYS */;
INSERT INTO `atributos` VALUES (2,'aaaa',39,14,11,0,55,22,46,17,43,16,24,6,47,18),(3,'Aaravos',14,2,19,4,8,1,5,3,10,0,4,3,20,5),(4,'analise',48,18,9,1,15,2,4,3,56,22,28,8,24,6),(5,'Alissa',18,4,20,5,18,4,18,4,20,5,17,3,19,4),(6,'Arya',18,4,16,3,15,2,12,1,10,0,8,1,14,2),(7,'Betumg',30,10,10,0,20,5,10,0,10,0,10,0,20,5),(8,'cain',20,5,8,1,16,3,8,1,8,1,14,2,8,1),(9,'calistro',14,2,20,5,12,1,14,2,12,1,10,0,20,5),(10,'clovis',10,0,10,0,10,0,10,0,10,0,10,0,10,0),(11,'Dante',18,4,18,4,18,4,18,4,18,4,18,4,18,4),(12,'Eragon',10,0,12,1,10,0,14,2,16,3,14,2,12,1),(13,'Ianatan',15,2,15,2,14,2,15,2,17,3,14,2,17,3),(14,'jorginho',20,5,20,5,10,0,20,5,14,2,10,0,22,6),(15,'Kalliope',18,3,11,0,10,0,12,1,10,0,10,0,15,3),(16,'Katarina',8,1,20,5,18,4,8,1,8,1,12,3,14,2),(17,'linguiça',6,2,7,2,15,2,15,2,15,2,5,3,14,1),(18,'Mali',8,0,10,0,14,2,20,5,16,3,12,1,8,1),(19,'Manuel',10,0,10,0,8,1,15,2,10,0,9,1,17,3),(20,'Mario',18,4,18,4,18,4,18,4,17,3,17,3,17,3),(21,'Maugrin',67,5,46,5,44,5,44,5,39,5,35,5,69,5),(22,'ptolomeu',60,5,50,5,40,5,50,5,40,5,50,5,50,5),(23,'Murtagh',11,0,12,1,14,2,20,5,12,1,8,1,14,2),(24,'nora',18,4,20,5,20,5,12,1,12,1,10,0,14,3),(25,'oscar',11,0,12,1,11,0,9,0,8,0,8,0,11,0),(41,'Zezim',15,2,16,3,20,5,10,0,8,-2,14,2,12,1);
/*!40000 ALTER TABLE `atributos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `idinventario` int(11) NOT NULL AUTO_INCREMENT,
  `item` varchar(50) DEFAULT NULL,
  `peso` decimal(4,2) DEFAULT NULL,
  `idpersonagem` int(11) DEFAULT NULL,
  PRIMARY KEY (`idinventario`),
  KEY `idpersonagem` (`idpersonagem`)
) ENGINE=MyISAM AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (2,'Pacotes de ervas   ',1.00,4),(3,'Aljava com 10 flechas   ',1.00,4),(4,'Carteira com moedas   ',1.00,4),(5,'ração ',1.00,4),(6,'10 peças de ouro  ',0.50,6),(7,'1 corda de 7m  ',3.50,6),(8,'viola que acalma os bixo  ',2.00,8),(9,'5 elixir roxo  ',3.00,8),(10,'1 mapa  ',0.00,8),(11,'3 elixir roxo   ',2.00,8),(12,'1  elixir de mana   ',1.00,8),(13,'4  elixir verde   ',4.00,8),(14,'Espada Curta  ',2.00,9),(15,'Adaga  ',0.50,9),(16,'Arco  ',1.00,11),(17,'Aljava com 20 flechas  ',1.00,11),(18,'Adaga  ',0.50,11),(19,'Arco  ',1.00,15),(20,'Aljava com 20 flechas  ',1.00,15),(21,'Plantas  ',1.00,15),(28,'Kit Médico  ',1.00,18),(29,'livro das bruxa  ',1.00,20),(30,'anel da fusao   ',0.50,20),(31,'ração ',1.00,20),(32,'pingente do maugrin  ',0.50,20),(33,'esfera da rapozinha  ',2.00,20),(34,'do maugrin  ',0.50,NULL),(35,'Dedo fura bolo do jovem jorge  ',0.50,21),(68,'armadura peitoral ',10.00,20),(67,' perola ',1.00,34),(66,' feijao ',2.00,34),(65,'carne ',5.00,34);
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pericias`
--

DROP TABLE IF EXISTS `pericias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pericias` (
  `personagempericias` varchar(30) DEFAULT NULL,
  `idpericias` int(11) NOT NULL AUTO_INCREMENT,
  `percepção` tinyint(4) DEFAULT NULL,
  `arremesso` tinyint(4) DEFAULT NULL,
  `lábia` tinyint(4) DEFAULT NULL,
  `convencer` tinyint(4) DEFAULT NULL,
  `pilotar` tinyint(4) DEFAULT NULL,
  `medicina` tinyint(4) DEFAULT NULL,
  `psicologia` tinyint(4) DEFAULT NULL,
  `atletismo` tinyint(4) DEFAULT NULL,
  `artes` tinyint(4) DEFAULT NULL,
  `domesticar` tinyint(4) DEFAULT NULL,
  `furtividade` tinyint(4) DEFAULT NULL,
  `estudo` tinyint(4) DEFAULT NULL,
  `crafting` tinyint(4) DEFAULT NULL,
  `primeirossocorros` tinyint(4) DEFAULT NULL,
  `acrobacia` tinyint(4) DEFAULT NULL,
  `arcanismo` tinyint(4) DEFAULT NULL,
  `natureza` tinyint(4) DEFAULT NULL,
  `trapaça` tinyint(4) DEFAULT NULL,
  `armasstr` tinyint(4) DEFAULT NULL,
  `armasdex` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`idpericias`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pericias`
--

LOCK TABLES `pericias` WRITE;
/*!40000 ALTER TABLE `pericias` DISABLE KEYS */;
INSERT INTO `pericias` VALUES ('Zezim',8,2,10,4,8,2,4,16,8,8,6,6,6,8,2,10,10,4,16,16,16);
/*!40000 ALTER TABLE `pericias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personagem`
--

DROP TABLE IF EXISTS `personagem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personagem` (
  `idpersonagem` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(30) DEFAULT NULL,
  `atributostable` int(11) DEFAULT NULL,
  `períciastable` int(11) DEFAULT NULL,
  `iddiscord` bigint(20) DEFAULT NULL,
  `embedCor` int(11) DEFAULT '0',
  `embedIcon` varchar(8000) DEFAULT 'ctx.guild.icon_url',
  `urlplanilha` varchar(8000) DEFAULT NULL,
  PRIMARY KEY (`idpersonagem`),
  KEY `atributostable` (`atributostable`),
  KEY `períciastable` (`períciastable`)
) ENGINE=MyISAM AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personagem`
--

LOCK TABLES `personagem` WRITE;
/*!40000 ALTER TABLE `personagem` DISABLE KEYS */;
INSERT INTO `personagem` VALUES (1,'Aaaa',2,NULL,877191808826875926,0,'ctx.guild.icon_url',NULL),(2,'Aaravos',3,NULL,NULL,0,'ctx.guild.icon_url',NULL),(3,'Analise',4,NULL,NULL,0,'ctx.guild.icon_url',NULL),(4,'Alissa',5,NULL,755941256877703199,16718146,' https://cdn.discordapp.com/attachments/868568667774926877/890984968031993856/96_Sem_Titulo_20210924085603.png','https://docs.google.com/spreadsheets/d/1ZS1H8Ce8Eq_RlJMsPxC0XnC-GMctqgKxAh2BA1OCM08/edit?usp=sharing'),(5,'Arya',6,NULL,861370102719840286,16776960,' https://images-ext-1.discordapp.net/external/p9vT4amT0JUWtY-tq-EiZAHtcuRsa2qP4FbqoZbSso0/%3Fsize%3D1024/https/cdn.discordapp.com/icons/868568667774926874/39af5a1ec81e4477447c891cf55cfbe7.webp?width',NULL),(6,'Betumg',7,NULL,872292098005663785,0,' https://media.discordapp.net/attachments/891076368471851029/892059658523648040/1eaa4959d22dae85ad3dac39a50649bc.jpg?width',NULL),(7,'Cain',8,NULL,NULL,0,'ctx.guild.icon_url',NULL),(8,'Calistro',9,NULL,621664265907994624,3801067,' https://cdn.discordapp.com/attachments/868568667774926877/893252961973706772/78b63fc50144e104c186253093ed7091.jpg',NULL),(9,'Clovis',10,NULL,710520700544352367,0,'ctx.guild.icon_url',NULL),(10,'Dante',11,NULL,NULL,0,'ctx.guild.icon_url',NULL),(11,'Eragon',12,NULL,732368768205979709,16776960,' https://images-ext-1.discordapp.net/external/p9vT4amT0JUWtY-tq-EiZAHtcuRsa2qP4FbqoZbSso0/%3Fsize%3D1024/https/cdn.discordapp.com/icons/868568667774926874/39af5a1ec81e4477447c891cf55cfbe7.webp?width','https://docs.google.com/spreadsheets/d/15Jwk7HpZaig_oj6Enn6tfjZqUJYQcd2viuy_8iMUFC0/edit?usp=sharing'),(12,'Ianatan',13,NULL,190513247462359041,0,'ctx.guild.icon_url',NULL),(13,'Jorginho',14,NULL,347716088458641408,6950317,' https://media.discordapp.net/attachments/812327180423921684/896484382284582942/unknown.png?width',NULL),(14,'Kalliope',15,NULL,755588126323245071,0,'ctx.guild.icon_url',NULL),(15,'Katarina',16,NULL,753034171055865888,0,'ctx.guild.icon_url',NULL),(16,'Linguiça',17,NULL,713402624585760778,0,'ctx.guild.icon_url',NULL),(17,'Mali',18,NULL,341700451168944138,16776960,' https://media.discordapp.net/attachments/884204336408854639/884229863723126814/141_Sem_Titulo_20210905211122.png?width',NULL),(18,'Manuel',19,NULL,866860420606328832,16776960,' https://media.discordapp.net/attachments/884153877295931402/884162458107904030/057.jpg?width',NULL),(19,'Mario',20,NULL,NULL,16776960,' https://media.discordapp.net/attachments/885626065156984903/885891647727091762/582810_OznuYiVS.png?width',NULL),(20,'Maugrin',21,NULL,675407695729131527,32768,' https://cdn.discordapp.com/attachments/872575672860700742/873666401406165002/5b9128be5b984ff3034ddb136a70c658.png','https://docs.google.com/spreadsheets/d/194P12H9b6_Pi06k3z9iYCyjZRJHX4dU2LG4PJHDed4k/edit?usp=sharing'),(21,'Ptolomeu',22,NULL,713822034878005288,255,' https://media.discordapp.net/attachments/872575672680349696/873668887554719754/dbfe070d4a951eae817617b86101d5ec-1.jpg?width','https://docs.google.com/spreadsheets/d/1kYjncY9l77tgbNy7nB0G2FSopDl1Njt6qnki7vMhtBk/edit?usp=sharing'),(22,'Murtagh',23,NULL,209453716892418049,16776960,' https://media.discordapp.net/attachments/883443704445161492/890290850335178832/images_-_2021-09-14T232503.589.jpeg?width',NULL),(23,'Nora',24,NULL,NULL,0,'ctx.guild.icon_url',NULL),(24,'Oscar',25,NULL,637830170807631892,0,'ctx.guild.icon_url',NULL),(34,'Zezim',41,8,NULL,0,'ctx.guild.icon_url',NULL),(35,'Kayser',NULL,NULL,753591462251200572,0,'ctx.guild.icon_url','https://docs.google.com/spreadsheets/d/1lg5OJCO7bHMPgCHZRFLzDh4FeX4A5p9hpym6WDvfRDc/edit#gid=0'),(36,'Targon',NULL,NULL,866196529718362122,0,'ctx.guild.icon_url','https://docs.google.com/spreadsheets/d/15FNo4d2cjpsy-Iora0JB49WQ6Db6L67i48LUq-KvoQo/edit#gid=0'),(37,'monstro_teste',NULL,NULL,NULL,0,'ctx.guild.icon_url','https://docs.google.com/spreadsheets/d/1IY3KHy0ZEoODqMDkmnGQc0Jr3Lzpk15CHavg6Gb-ml8/edit#gid=0'),(38,'monstro monstro_teste',NULL,NULL,NULL,0,'ctx.guild.icon_url','https://docs.google.com/spreadsheets/d/1IY3KHy0ZEoODqMDkmnGQc0Jr3Lzpk15CHavg6Gb-ml8/edit#gid=0'),(39,'Edward',NULL,NULL,539356197829214226,0,'ctx.guild.icon_url',NULL),(40,'Suli',NULL,NULL,879524527409872937,0,'ctx.guild.icon_url',NULL),(41,'linskin',NULL,NULL,846489224395358252,0,'ctx.guild.icon_url',NULL),(42,'Victor',NULL,NULL,458947104216186880,0,'ctx.guild.icon_url',NULL),(43,'Joseph',NULL,NULL,498618686991499264,0,'ctx.guild.icon_url',NULL),(44,'Maya',NULL,NULL,685633794929459257,0,'ctx.guild.icon_url',NULL),(45,'Jonny',NULL,NULL,468917082700906496,0,'ctx.guild.icon_url',NULL);
/*!40000 ALTER TABLE `personagem` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-24 18:52:48
