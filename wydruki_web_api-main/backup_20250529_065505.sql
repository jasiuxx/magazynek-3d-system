/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.5.28-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: 192.168.101.100    Database: Druk_3D
-- ------------------------------------------------------
-- Server version	10.5.18-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add wydruki',7,'add_wydruki'),(26,'Can change wydruki',7,'change_wydruki'),(27,'Can delete wydruki',7,'delete_wydruki'),(28,'Can view wydruki',7,'view_wydruki'),(29,'Can add pracownicy',8,'add_pracownicy'),(30,'Can change pracownicy',8,'change_pracownicy'),(31,'Can delete pracownicy',8,'delete_pracownicy'),(32,'Can view pracownicy',8,'view_pracownicy'),(33,'Can add pobrania',9,'add_pobrania'),(34,'Can change pobrania',9,'change_pobrania'),(35,'Can delete pobrania',9,'delete_pobrania'),(36,'Can view pobrania',9,'view_pobrania');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$7YCcslrWI5s4Yl3Ctcy033$8kjQOeEhC6oeXRVp5dwNLEamAVqYK4CKXxSXyzBbR2M=',NULL,1,'admin','','','jan.szczudlo@hkl.eu',1,1,'2025-05-14 06:17:28.588004');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(9,'panel_wydrukow','pobrania'),(8,'panel_wydrukow','pracownicy'),(7,'panel_wydrukow','wydruki'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-05-14 06:16:44.358956'),(2,'auth','0001_initial','2025-05-14 06:16:44.715019'),(3,'admin','0001_initial','2025-05-14 06:16:44.796764'),(4,'admin','0002_logentry_remove_auto_add','2025-05-14 06:16:44.822429'),(5,'admin','0003_logentry_add_action_flag_choices','2025-05-14 06:16:44.851389'),(6,'contenttypes','0002_remove_content_type_name','2025-05-14 06:16:44.910711'),(7,'auth','0002_alter_permission_name_max_length','2025-05-14 06:16:44.954980'),(8,'auth','0003_alter_user_email_max_length','2025-05-14 06:16:44.992011'),(9,'auth','0004_alter_user_username_opts','2025-05-14 06:16:45.017851'),(10,'auth','0005_alter_user_last_login_null','2025-05-14 06:16:45.055414'),(11,'auth','0006_require_contenttypes_0002','2025-05-14 06:16:45.058943'),(12,'auth','0007_alter_validators_add_error_messages','2025-05-14 06:16:45.087970'),(13,'auth','0008_alter_user_username_max_length','2025-05-14 06:16:45.153639'),(14,'auth','0009_alter_user_last_name_max_length','2025-05-14 06:16:45.242032'),(15,'auth','0010_alter_group_name_max_length','2025-05-14 06:16:45.270953'),(16,'auth','0011_update_proxy_permissions','2025-05-14 06:16:45.299375'),(17,'auth','0012_alter_user_first_name_max_length','2025-05-14 06:16:45.333885'),(18,'panel_wydrukow','0001_initial','2025-05-14 06:16:45.351672'),(19,'sessions','0001_initial','2025-05-14 06:16:45.371428');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pobrania`
--

DROP TABLE IF EXISTS `pobrania`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pobrania` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wydruk_id` int(11) NOT NULL,
  `pracownicy_id` int(11) DEFAULT NULL,
  `identyfikator` varchar(30) DEFAULT NULL,
  `imie_pracownika` varchar(30) DEFAULT NULL,
  `nazwisko_pracownika` varchar(30) DEFAULT NULL,
  `ilosc` int(11) NOT NULL,
  `data_pobrania` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `wydruk_id` (`wydruk_id`),
  KEY `pracownicy_id` (`pracownicy_id`),
  CONSTRAINT `pobrania_ibfk_1` FOREIGN KEY (`wydruk_id`) REFERENCES `wydruki` (`id`),
  CONSTRAINT `pobrania_ibfk_2` FOREIGN KEY (`pracownicy_id`) REFERENCES `pracownicy` (`pracownicy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pobrania`
--

LOCK TABLES `pobrania` WRITE;
/*!40000 ALTER TABLE `pobrania` DISABLE KEYS */;
/*!40000 ALTER TABLE `pobrania` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pracownicy`
--

DROP TABLE IF EXISTS `pracownicy`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pracownicy` (
  `pracownicy_id` int(11) NOT NULL AUTO_INCREMENT,
  `imie_pracownika` varchar(30) DEFAULT NULL,
  `nazwisko_pracownika` varchar(30) DEFAULT NULL,
  `dzial` varchar(30) DEFAULT NULL,
  `identyfikator` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`pracownicy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=464 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pracownicy`
--

LOCK TABLES `pracownicy` WRITE;
/*!40000 ALTER TABLE `pracownicy` DISABLE KEYS */;
INSERT INTO `pracownicy` VALUES (1,'Jarosław','Janiec','Dłużyca','000445'),(2,'Janusz','Bajkowski','Dłużyca','001645'),(4,'Andrii','Driuk','Dłużyca','003346'),(5,'Adrian','Zajączkowski','Dłużyca','001704'),(6,'Vasyl','Galischuk','Dłużyca','001680'),(7,'Mariusz','Łysiak','Dłużyca','002083'),(8,'Ihor','Midzyan','Dłużyca','000839'),(9,'Andrii','Isaienko','Dłużyca','003200'),(10,'Dariusz','Sołtys','Dłużyca','000588'),(11,'Dmytro','Davydenko','Dłużyca','000812'),(12,'Tamang Man','Bahadur','Dłużyca','001032'),(13,'Rinjee','Sherpa','Dłużyca','003263'),(14,'Kuba','Kowalczyk','Magazyn',NULL),(15,'Kacper','Orpel','Magazyn','001608'),(16,'Monika','Bogusławska','Magazyn','000886'),(17,'Paulina','Dzień','Magazyn','000885'),(18,'Ania','Relisko','Magazyn','003096'),(19,'Ania','Malec','Magazyn','000353'),(20,'Konstantyn','Mykhailovsky','Magazyn','003458'),(21,'Bikram','Tamang','Dłużyca','003121'),(22,'Ayoub','Hallad','Magazyn','003459'),(30,'Rachid','Belghiat','Magazyn','003326'),(31,'Izabela','Białas','Magazyn','000751'),(32,'Cezary','Brzeziński','Magazyn','001404'),(33,'Karolina','Raunmiagi','Magazyn','000618'),(34,'Grzegorz','Fromhut','Magazyn','003177'),(64,'Anna','Matuszewska','Kontrola',''),(65,'Piotr','Andrelczyk','Pakowanie','000661'),(66,'Katarzyna','Błażejczak','Wzorniki','000366'),(69,'Renata','Józefowicz','Pakowanie','001731'),(70,'Artem','Kolundaiev','Pakowanie','001093'),(71,'Birendra','Lama','Rolety','000868'),(72,'Dmytro','Melnykov','Pakowanie','003058'),(73,'Agnieszka','Minda','Pakowanie','000541'),(74,'Larysa','Radzivil','Pakowanie','003302'),(75,'Anna','Seliga','Żaluzje Drewniane','000655'),(76,'Anna','Wełpa','Inne',''),(77,'Milan','Lamichhane','Pakowanie','003489'),(78,'Pavlo','Mahera','Pakowanie','002937'),(79,'Stephen Villaflores','San Agustin','Pakowanie','003520'),(161,'Grzegorz','Krasucki','Skosy','000619'),(162,'Hanna','Sierakowska','Skosy','002958'),(164,'Bogusław','Steczyński','Utrzymanie Ruchu','002057'),(165,'Andrzej','Wiśniewski','Utrzymanie Ruchu',''),(166,'Jarosław','Wiśniewski','Utrzymanie Ruchu',''),(167,'Aniela','Budzińska','Vertikale','000363'),(170,'Valdyslav','Mandryka','Vertikale','000967'),(171,'Viktoriia','Skyba','Vertikale','002107'),(172,'Oleksandr','Staroverets','Vertikale','003530'),(173,'Klaudia','Kurkowska','Wzorniki','001161'),(175,'Ilona','Polańska','Wzorniki','000729'),(178,'Jolanta','Tomczyk','Wzorniki','000656'),(179,'Zofia','Zduńczyk','Wzorniki','000688'),(209,'Daria','Brazhenko','Żaluzje Drewniane','002137'),(210,'Serhii','Chernov','Żaluzje Drewniane','001715'),(212,'Marzena','Flejterska','Żaluzje Drewniane','001496'),(213,'Sabina','Flejterska','Żaluzje Drewniane','000495'),(215,'Olena','Hosudarska','Żaluzje Drewniane','001024'),(216,'Kateryna','Hrytsai','Inne','002071'),(217,'Żaneta','Imiela','Żaluzje Drewniane','000300'),(218,'Iryna','Kalishnichenko','Żaluzje Drewniane','002994'),(219,'Edyta','Kostrzewa','Żaluzje Drewniane','000602'),(220,'Alena','Krauchenia','Żaluzje Drewniane','003223'),(221,'Dorota','Kuchniak','Żaluzje Drewniane','000373'),(223,'Yuliia','Nortseva','Żaluzje Drewniane','002939'),(224,'Mirosław','Rabe','Żaluzje Drewniane','002240'),(226,'Rebeka','Rebeka','Żaluzje Drewniane','003176'),(228,'Maiia','Shkurat','Żaluzje Drewniane','003309'),(229,'Tetiana','Strilchuk','Żaluzje Drewniane','003099'),(230,'Iwona','Suwalska','Żaluzje Drewniane','000547'),(231,'Hanna','Syvak','Żaluzje Drewniane','003292'),(233,'Viktoriia','Volkova','Żaluzje Drewniane','003380'),(234,'Maryna','Vyshniakova','Żaluzje Drewniane','001907'),(236,'Iryna','Khriashchevska','Żaluzje Drewniane','003493'),(237,'Yuliia','Povelytsia','Żaluzje Drewniane','003480'),(239,'Natalia','Bay-Robak','Plisy','002962'),(240,'Anna','Boguszewicz','Plisy','000836'),(241,'Kateryna','Burenko','Plisy','000909'),(242,'Yuliia','Davydenko','Plisy','000838'),(243,'Katarzyna','Florjańczyk-Michalska','Plisy','002095'),(244,'Anna','Guss','Plisy','000339'),(245,'Marzena','Guzik','Plisy','000513'),(246,'Tatiana','Isaienko','Plisy','001764'),(247,'Dorota','Kamińska','Plisy','000654'),(248,'Olena','Kramarenko','Plisy','000931'),(249,'Monika','Krupińska','Plisy','001206'),(250,'Ewa','Kucharczuk','Plisy','000516'),(251,'Joanna','Kujawka','Plisy','000686'),(252,'Anastasiia','Kukurudza','Plisy','001807'),(253,'Sylwia','Kulińska','Plisy','000335'),(254,'Kacper','Kuniszek','Plisy','000540'),(255,'Tetiana','Kunytska','Plisy','001884'),(256,'Nataliia','Kuprata','Plisy','000764'),(257,'Bimala','Lama','Plisy','003209'),(258,'Agnieszka','Michalska','Plisy','000332'),(259,'Iryna','Midzyan','Plisy','000840'),(260,'Anna','Nazdrowicz','Plisy','000448'),(261,'Małgorzata','Nowak','Plisy','001406'),(262,'Renata','Piasecka','Plisy','000221'),(263,'Sylwia','Raczyńska','Plisy','000447'),(264,'Maryna','Reva','Plisy',''),(265,'Agnieszka','Samson','Inne',''),(266,'Tatsiana','Sharkievich','Plisy',''),(267,'Paulina','Sikora','Plisy',''),(268,'Agnieszka','Skrzypa','Plisy',''),(271,'Elżbieta','Śluz','Plisy',''),(272,'Irena','Talarek','Plisy',''),(273,'Nataliia','Volyk','Plisy',''),(274,'Anna','Wasilewska','Plisy',''),(275,'Kinga','Wiśniewska-Rodzeń','Plisy',''),(276,'Olena','Yankovska','Inne',''),(282,'Yaroslav','Honcharuk','Inne',''),(283,'Anna','Kozachek','Plisy',''),(284,'Iryna','Osipova','Plisy',''),(285,'Vladyslav','Rudnitskyi','Plisy',''),(286,'Veronika','Surdulenko','Plisy',''),(288,'Natalia','Tykhonova','Inne',''),(289,'Anna','Farbotko','Raffrollo','000543'),(290,'Urszula','Iliminowicz','Raffrollo','000581'),(291,'Kinga','Kamionka','Raffrollo','000312'),(292,'Brygida','Krzysanowska','Raffrollo','003240'),(295,'Halyna','Metanovska','Raffrollo','001283'),(296,'Marlena','Misiak','Raffrollo','000386'),(297,'Beata','Moskwa','Raffrollo','000752'),(298,'Ewa','Ruda','Raffrollo','000188'),(299,'Katarzyna','Sadowska','Raffrollo','000689'),(300,'Ewa','Trzcińska','Raffrollo','001374'),(301,'Monika','Urbańska','Raffrollo','000182'),(304,'Nadiia','Yavorska','Raffrollo','003340'),(305,'Daniel','Skowroński','Plisy',''),(306,'Yuliia','Dorozhon','Plisy',''),(307,'Małgorzata','Aksamit','Rolety','002075'),(308,'Maryna','Babenko','Rolety','001622'),(309,'Beata','Bąk','Rolety','001444'),(310,'Tetiana','Bubela','Rolety','003155'),(311,'Iwona','Bulsa','Żaluzje Drewniane','000439'),(312,'Paulina','Czepielkiewicz','Rolety','000446'),(313,'Yana','Hrabovska','Rolety','001665'),(314,'Anna','Klen','Rolety','000468'),(315,'Maciej','Koszelak','Rolety','000372'),(316,'Joanna','Ostrzycka','Inne',''),(317,'Agnieszka','Pasieka','Żaluzje Drewniane','000545'),(318,'Yuliia','Sedina','Inne',''),(319,'Iwona','Wojtkowska','Rolety','000101'),(323,'Mariia','Rabosh','Rolety','003476'),(324,'Anna','Ścigała','Rolety','000544'),(325,'Anna','Sukha','Inne',''),(332,'Klaudia','Gomółka','Żaluzje 25mm','003311'),(334,'Agnieszka','Kolokajtys-Berdzik','Żaluzje 25mm','000136'),(335,'Inna','Klimenko','Inne',''),(338,'Svitlana','Kotsiubynska','Żaluzje 25mm','003334'),(339,'Yuliia','Koval','Rolety','001754'),(340,'Agnieszka','Kubus','Żaluzje 25mm','003473'),(341,'Ewa','Lisiecka','Żaluzje 25mm','001868'),(344,'Agnieszka','Piekarska','Żaluzje 25mm','003422'),(345,'Iryna','Shnaider','Żaluzje 25mm','003410'),(346,'Dorota','Stawicka','Żaluzje 25mm','000482'),(347,'Gabriela','Stefańska','Żaluzje 25mm','002220'),(348,'Halyna','Tsitsiura','Żaluzje 25mm','001041'),(349,'Yeliena','Varnavska','Żaluzje 25mm','002188'),(350,'Kateryna','Vozniuk','Żaluzje Drewniane','003182'),(351,'Tetiana','Bahlikova','Żaluzje 25mm','002008'),(352,'Iryna','Bakhur','Żaluzje 25mm','003514'),(353,'Anjeannette Requillas','Bayaban','Żaluzje 25mm','003521'),(356,'Yuliia','Solovei','Inne',''),(357,'Jan Rose Condrillon','Taneo','Żaluzje 25mm','003507'),(360,'Monika','Stefaniuk-Konwerska','Pakowanie','002046'),(362,'Tomasz','Kurkowski','Utrzymanie Ruchu',''),(365,'Izabela','Rojek','Żaluzje Drewniane','000352'),(366,'Patrycja','Tinelt','Żaluzje Drewniane','001251'),(367,'Tomasz','Fit','Pakowanie','000119'),(368,'Agnieszka','Prokopiuk','Plisy',''),(369,'Arkadiusz','Jankowski','Plisy',''),(370,'Mariola','Krzysztanowicz','Raffrollo','000185'),(371,'Wioletta','Wójcik','Raffrollo','002976'),(372,'Aurelia','Dziadosz','Skosy','000131'),(374,'Aurelia','Sołtys','Wzorniki','000164'),(375,'Renata','Kurkowska','Wzorniki','000165'),(376,'Teresa','Sękowska','Wzorniki','000124'),(377,'Ewa','Wójcik','Żaluzje 25mm','002973'),(378,'Natalia','Chupryna','Żaluzje 25mm','000611'),(381,'Kateryna','Kovalenko','Inne',''),(383,'Maryna','Papu','Rolety','003533'),(384,'Olena','Malakhova','Rolety','003535'),(385,'Liubov','Lohina','Plisy',''),(386,'Oryna','Kharlamova','Inne',''),(387,'Hanna','Kovalova','Pakowanie','003537'),(388,'MICAH','ZAGADO JUARBAL','Rolety','003540'),(393,'Laptieva','Halyna','Inne',''),(395,'Antonina','Dereza','Inne',''),(396,'Zlata','Kozyr','Inne',''),(397,'Nikola','Pilipczuk','Skosy','003542'),(398,'Olena','Repushevska','Żaluzje Drewniane','003551'),(401,'Maria Cristina','Rivas Balicot','Żaluzje 25mm','003554'),(402,'Larysa','Rabota','Żaluzje Drewniane','001902'),(403,'Alona','Chernukhina','Żaluzje 25mm','003556'),(409,'Adrian','Migdał','Dłużyca','000008'),(410,'Edelyn','Gomez Miranday','Żaluzje 25mm',NULL),(413,'Rafael','Cantoba Abelay','Pakowanie',NULL),(414,'Grzegorz','Robak','RD','000111'),(415,'Piotr','Janiak','RD',NULL),(417,'Katarzyna','Cieśla','Biuro',NULL),(418,'Elżbieta','Dąbrowska','Biuro',NULL),(419,'Anna','Handke','Inne',NULL),(420,'Marta','Juścińska','Kadry',NULL),(421,'Anna','Pacocha','Biuro',NULL),(422,'Lucyna','Pajek','Kadry',NULL),(423,'Milena','Rozalska','Biuro',NULL),(424,'Paulina','Wasilewska','Biuro',NULL),(425,'Małgorzata','Hasinec','Inne',NULL),(426,'Agnieszka','Korzeniewska','Inne',NULL),(427,'Rafał','Woźniak','Inne',NULL),(428,'Katarzyna','Dolecka','Biuro1',NULL),(429,'Martyna','Gabska','Biuro1',NULL),(430,'Urszula','Jończyk-Gajdzińska','Biuro1',NULL),(431,'Roksana','Rysiowska','Biuro1',NULL),(432,'Mirosław','Bujalski','IT',NULL),(433,'Grzegorz','Fijałkowski','IT',NULL),(434,'Piotr','Gawdzik','IT',NULL),(435,'Roman','Kałka','IT',NULL),(436,'Rafał','Kozłowski','IT',NULL),(437,'Paweł','Woroniecki','IT',NULL),(438,'Bernadeta','Kłosińska','Rolety','000745'),(452,'Jan','Szczudło','RD','003565'),(454,'ARIS BERNARD','GUARIN ALIMAY','Rolety','003539'),(455,'Cabanes','Clifford Abapo','Rolety',''),(456,'JENNIFER','TABANGIN ABELLA','Żaluzje Drewniane',''),(457,'STEPHAN MICHAEL','ARISTO BAYLEY','Pakowanie',''),(458,'Mirela','Ptaszynska','Biuro',''),(459,'Kinga','Marchlewska','Raffrollo','000657'),(460,'Natalia','Skrzypa','Pakowanie',''),(461,'Devimai','Tamang','Żaluzje Drewniane',''),(462,'Andrii','Krit','Vertikale',''),(463,'Chrystian','Bolesta','Dłużyca','');
/*!40000 ALTER TABLE `pracownicy` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pracownicy_backup`
--

DROP TABLE IF EXISTS `pracownicy_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pracownicy_backup` (
  `pracownicy_id` int(11) NOT NULL AUTO_INCREMENT,
  `imie_pracownika` varchar(30) NOT NULL,
  `nazwisko_pracownika` varchar(30) NOT NULL,
  `dzial` varchar(30) NOT NULL,
  `identyfikator` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`pracownicy_id`),
  UNIQUE KEY `imie_pracownika` (`imie_pracownika`,`nazwisko_pracownika`),
  KEY `idx_identyfikator` (`identyfikator`)
) ENGINE=InnoDB AUTO_INCREMENT=453 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pracownicy_backup`
--

LOCK TABLES `pracownicy_backup` WRITE;
/*!40000 ALTER TABLE `pracownicy_backup` DISABLE KEYS */;
INSERT INTO `pracownicy_backup` VALUES (1,'Jarosław','Janiec','Dłużyca','000445'),(2,'Janusz','Bajkowski','Dłużyca','001645'),(4,'Andrii','Driuk','Dłużyca','003346'),(5,'Adrian','Zajączkowski','Dłużyca','001704'),(6,'Vasyl','Galischuk','Dłużyca','001680'),(7,'Mariusz','Łysiak','Dłużyca','002083'),(8,'Ihor','Midzyan','Dłużyca','000839'),(9,'Andrii','Isaienko','Dłużyca','003200'),(10,'Dariusz','Sołtys','Dłużyca','000588'),(11,'Dmytro','Davydenko','Dłużyca','000812'),(12,'Tamang Man','Bahadur','Dłużyca','001032'),(13,'Rinjee','Sherpa','Dłużyca','003263'),(14,'Kuba','Kowalczyk','Magazyn',''),(15,'Kacper','Orpel','Magazyn',''),(16,'Monika','Bogusławska','Magazyn',''),(17,'Paulina','Dzień','Magazyn',''),(18,'Ania','Relisko','Magazyn',''),(19,'Ania','Malec','Magazyn',''),(20,'Konstantyn','Mykhailovsky','Magazyn',''),(21,'Bikram','Tamang','Dłużyca',''),(22,'Ayoub','Hallad','Magazyn',''),(30,'Rachid','Belghiat','Magazyn',''),(31,'Izabela','Białas','Magazyn',''),(32,'Cezary','Brzeziński','Magazyn',''),(33,'Karolina','Raunmiagi','Magazyn',''),(34,'Grzegorz','Frohmut','Magazyn',''),(64,'Anna','Matuszewska','Kontrola',''),(65,'Piotr','Andrelczyk','Pakowanie',''),(66,'Katarzyna','Błażejczak','Wzorniki',''),(69,'Renata','Józefowicz','Pakowanie',''),(70,'Artem','Kolundaiev','Pakowanie',''),(71,'Birendra','Lama','Rolety',''),(72,'Dmytro','Melnykov','Pakowanie',''),(73,'Agnieszka','Minda','Pakowanie',''),(74,'Larysa','Radzivill','Pakowanie',''),(75,'Anna','Seliga','Pakowanie',''),(76,'Anna','Wetpa','Pakowanie',''),(77,'Milan','Lamichhane','Pakowanie',''),(78,'Pavlo','Mahera','Pakowanie',''),(79,'Stephen Villaflores','San Agustin','Pakowanie',''),(80,'Artem','Tkachuk','Pakowanie',''),(161,'Grzegorz','Krasucki','Skosy',''),(162,'Hanna','Sierakowska','Skosy',''),(164,'Bogusław','Steczyński','Utrzymanie Ruchu',''),(165,'Andrzej','Wiśniewski','Utrzymanie Ruchu',''),(166,'Jarosław','Wiśniewski','Utrzymanie Ruchu',''),(167,'Aniela','Budzińska','Vertikale',''),(170,'Valdyslav','Mandryka','Vertikale',''),(171,'Viktoriia','Skyba','Vertikale',''),(172,'Oleksandr','Staroverets','Vertikale',''),(173,'Klaudia','Kurkowska','Wzorniki',''),(175,'Ilona','Polańska','Wzorniki',''),(178,'Jolanta','Tomczyk','Wzorniki',''),(179,'Zofia','Zduńczyk','Wzorniki',''),(209,'Daria','Brazhenko','Żaluzje Drewniane',''),(210,'Serhii','Chernov','Żaluzje Drewniane',''),(212,'Marzena','Flejterska','Żaluzje Drewniane',''),(213,'Sabina','Flejterska','Żaluzje Drewniane',''),(214,'Svitlana','Harauskaya','Żaluzje Drewniane',''),(215,'Olena','Hosudarska','Żaluzje Drewniane',''),(216,'Kateryna','Hrytsai','Żaluzje Drewniane',''),(217,'Żaneta','Imiela','Żaluzje Drewniane',''),(218,'Iryna','Kolishnichenko','Żaluzje Drewniane',''),(219,'Edyta','Kostrzewa','Żaluzje Drewniane',''),(220,'Alena','Krauchenia','Żaluzje Drewniane',''),(221,'Dorota','Kuchniak','Żaluzje Drewniane',''),(223,'Yuliia','Nortseva','Żaluzje Drewniane',''),(224,'Mirosław','Rabe','Żaluzje Drewniane',''),(226,'Rebekah','Rebekah','Żaluzje Drewniane',''),(228,'Maiia','Shkurat','Żaluzje Drewniane',''),(229,'Tetiana','Strilchuk','Żaluzje Drewniane',''),(230,'Iwona','Suwalska','Żaluzje Drewniane',''),(231,'Hanna','Syvak','Żaluzje Drewniane',''),(233,'Viktoriia','Volkova','Żaluzje Drewniane',''),(234,'Maryna','Vyshniakova','Żaluzje Drewniane',''),(235,'Nadiia','Karachun','Żaluzje Drewniane',''),(236,'Iryna','Khriashchevska','Żaluzje Drewniane',''),(237,'Yuliia','Povelytsia','Żaluzje Drewniane',''),(239,'Natalia','Bay-Robak','Plisy',''),(240,'Anna','Boguszewicz','Plisy',''),(241,'Kateryna','Burenko','Plisy',''),(242,'Yuliia','Davydenko','Plisy',''),(243,'Katarzyna','Florjańczyk-Michalska','Plisy',''),(244,'Anna','Guss','Plisy',''),(245,'Marzena','Guzik','Plisy',''),(246,'Tatiana','Isaienko','Plisy',''),(247,'Dorota','Kamińska','Plisy',''),(248,'Olena','Kramarenko','Plisy',''),(249,'Monika','Krupińska','Plisy',''),(250,'Ewa','Kucharczuk','Plisy',''),(251,'Joanna','Kujawka','Plisy',''),(252,'Anastasiia','Kukurudza','Plisy',''),(253,'Sylwia','Kulińska','Plisy',''),(254,'Kacper','Kuniszek','Plisy',''),(255,'Tetiana','Kunytska','Plisy',''),(256,'Nataliia','Kuprata','Plisy',''),(257,'Bimala','Lama','Plisy',''),(258,'Agnieszka','Michalska','Plisy',''),(259,'Iryna','Midzyan','Plisy',''),(260,'Anna','Nazdrowicz','Plisy',''),(261,'Małgorzata','Nowak','Plisy',''),(262,'Renata','Piasecka','Plisy',''),(263,'Sylwia','Raczyńska','Plisy',''),(264,'Maryna','Reva','Plisy',''),(265,'Agnieszka','Samson','Inne',''),(266,'Tatsiana','Sharkievich','Plisy',''),(267,'Paulina','Sikora','Plisy',''),(268,'Agnieszka','Skrzypa','Plisy',''),(271,'Elżbieta','Śluz','Plisy',''),(272,'Irena','Talarek','Plisy',''),(273,'Nataliia','Volyk','Plisy',''),(274,'Anna','Wasilewska','Plisy',''),(275,'Kinga','Wiśniewska-Rodzeń','Plisy',''),(276,'Olena','Yankovska','Inne',''),(282,'Yaroslav','Honcharuk','Inne',''),(283,'Anna','Kozachek','Plisy',''),(284,'Iryna','Osipova','Plisy',''),(285,'Vladyslav','Rudnitskyi','Plisy',''),(286,'Veronika','Surdulenko','Plisy',''),(288,'Natalia','Tykhonova','Plisy',''),(289,'Anna','Farbotko','Raffrollo',''),(290,'Urszula','Iliminowicz','Raffrollo',''),(291,'Kinga','Kamionka','Raffrollo',''),(292,'Brygida','Krzysanowska','Raffrollo',''),(295,'Halyna','Metanovska','Raffrollo',''),(296,'Marlena','Misiak','Raffrollo',''),(297,'Beata','Moskwa','Raffrollo',''),(298,'Ewa','Ruda','Raffrollo',''),(299,'Katarzyna','Sadowska','Raffrollo',''),(300,'Ewa','Trzcińska','Raffrollo',''),(301,'Monika','Urbańska','Raffrollo',''),(304,'Nadiia','Yavorska','Raffrollo',''),(305,'Daniel','Skowroński','Plisy',''),(306,'Yuliia','Dorozhon','Plisy',''),(307,'Małgorzata','Aksamit','Rolety',''),(308,'Maryna','Babenko','Rolety',''),(309,'Beata','Bąk','Rolety',''),(310,'Tetiana','Bubela','Rolety',''),(311,'Iwona','Bulsa','Rolety',''),(312,'Paulina','Czepielkiewicz','Rolety',''),(313,'Yana','Hrabovska','Rolety',''),(314,'Anna','Klen','Rolety',''),(315,'Maciej','Koszelak','Rolety',''),(316,'Joanna','Ostrzycka','Inne',''),(317,'Agnieszka','Pasieka','Żaluzje Drewniane',''),(318,'Yuliia','Sedina','Inne',''),(319,'Iwona','Wojtkowska','Rolety',''),(323,'Mariia','Rabosh','Rolety',''),(324,'Anna','Ścigała','Rolety',''),(325,'Anna','Sukha','Plisy',''),(332,'Klaudia','Gomółka','Żaluzje 25mm',''),(334,'Agnieszka','Kolokajtys-Berdzik','Żaluzje 25mm',''),(335,'Inna','Klimenko','Inne',''),(338,'Svitlana','Kotsiubynska','Żaluzje 25mm',''),(339,'Yuliia','Koval','Inne',''),(340,'Agnieszka','Kubus','Żaluzje 25mm',''),(341,'Ewa','Lisiecka','Żaluzje 25mm',''),(344,'Agnieszka','Piekarska','Żaluzje 25mm',''),(345,'Iryna','Shnaider','Żaluzje 25mm',''),(346,'Dorota','Stawicka','Żaluzje 25mm',''),(347,'Gabriela','Stefańska','Żaluzje 25mm',''),(348,'Halyna','Tsitsiura','Żaluzje 25mm',''),(349,'Yeliena','Varnavska','Żaluzje 25mm',''),(350,'Kateryna','Vozniuk','Żaluzje Drewniane',''),(351,'Tetiana','Bahlikova','Żaluzje 25mm',''),(352,'Iryna','Bakhur','Żaluzje 25mm',''),(353,'Anjeannette Requillas','Bayaban','Żaluzje 25mm',''),(356,'Yuliia','Solovei','Inne',''),(357,'Jan Rose Condrillon','Taneo','Żaluzje 25mm',''),(360,'Monika','Stefaniuk-Konwerska','Pakowanie',''),(362,'Tomasz','Kurkowski','Utrzymanie Ruchu',''),(363,'Ewa','Kęszka','Rolety',''),(364,'Katarzyna','Zalewska','Rolety',''),(365,'Izabela','Rojek','Żaluzje Drewniane',''),(366,'Patrycja','Tinelt','Żaluzje Drewniane',''),(367,'Tomasz','Fit','Pakowanie',''),(368,'Agnieszka','Prokopiuk','Plisy',''),(369,'Arkadiusz','Jankowski','Plisy',''),(370,'Mariola','Krzysztanowicz','Raffrollo',''),(371,'Wioletta','Wójcik','Raffrollo',''),(372,'Aurelia','Dziadosz','Skosy',''),(373,'Andrii','Krit','Vertikale',''),(374,'Aurelia','Sołtys','Wzorniki',''),(375,'Renata','Kurkowska','Wzorniki',''),(376,'Teresa','Sękowska','Wzorniki',''),(377,'Ewa','Wójcik','Żaluzje 25mm',''),(378,'Natalia','Chupryna','Żaluzje 25mm',''),(381,'Kateryna','Kovalenko','Inne',''),(383,'Maryna','Papu','Rolety',''),(384,'Olena','Malakhova','Rolety',''),(385,'Liubov','Lohina','Plisy',''),(386,'Oryna','Kharlamova','Inne',''),(387,'Hanna','Kovalova','Pakowanie',''),(388,'MICAH','ZAGADO JUARBAL','Rolety',''),(389,'ARIS','BERNARD GUARIN ALIMAY','Rolety',''),(390,'Hlib','Povelytsia','Dłużyca',''),(393,'Laptieva','Halyna','Inne',''),(395,'Antonina','Dereza','Inne',''),(396,'Zlata','Kozyr','Inne',''),(397,'Nikola','Pilipczuk','Skosy',''),(398,'Olena','Repushevska','Żaluzje Drewniane',''),(399,'Zuzanna','Świrska','Żaluzje Drewniane',''),(401,'Maria Cristina','Rivas Balicot','Żaluzje 25mm',''),(402,'Larysa','Roboty','Żaluzje Drewniane',''),(403,'Alona','Chernukhina','Żaluzje 25mm',''),(404,'NAZAR','KARACHUN','Inne',''),(409,'Adrian','Migdał','Dłużyca',NULL),(410,'Edelyn','Gomez Miranday','Żaluzje 25mm',NULL),(412,'Grigorii','Scetinnicov ','Magazyn',NULL),(413,'Rafael','Cantoba Abelay','Pakowanie',NULL),(414,'Grzegorz','Robak','RD','000111'),(415,'Piotr','Janiak','RD',NULL),(416,'Katarzyna','Alama','Biuro',NULL),(417,'Katarzyna','Cieśla','Biuro',NULL),(418,'Elżbieta','Dąbrowska','Biuro',NULL),(419,'Anna','Handke','Biuro',NULL),(420,'Marta','Juścińska','Biuro',NULL),(421,'Anna','Pacocha','Biuro',NULL),(422,'Lucyna','Pajek','Biuro',NULL),(423,'Milena','Rozalska','Biuro',NULL),(424,'Paulina','Wasilewska','Biuro',NULL),(425,'Małgorzata','Hasinec','Biuro',NULL),(426,'Agnieszka','Korzeniewska','Biuro',NULL),(427,'Rafał','Woźniak','Biuro',NULL),(428,'Katarzyna','Dolecka','Biuro1',NULL),(429,'Martyna','Gabska','Biuro1',NULL),(430,'Urszula','Jończyk-Gajdzińska','Biuro1',NULL),(431,'Roksana','Rysiowska','Biuro1',NULL),(432,'Mirosław','Bujalski','IT',NULL),(433,'Grzegorz','Fijałkowski','IT',NULL),(434,'Piotr','Gawdzik','IT',NULL),(435,'Roman','Kałka','IT',NULL),(436,'Rafał','Kozłowski','IT',NULL),(437,'Paweł','Woroniecki','IT',NULL),(438,'Bernadeta','Kłosińska','Rolety',NULL),(452,'Jan','Szczudło','RD','003565');
/*!40000 ALTER TABLE `pracownicy_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wydruki`
--

DROP TABLE IF EXISTS `wydruki`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `wydruki` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kod` varchar(50) NOT NULL,
  `opis` text DEFAULT NULL,
  `ilosc` int(11) NOT NULL DEFAULT 0,
  `szt_w_wor` int(11) NOT NULL DEFAULT 1,
  `stan` int(11) GENERATED ALWAYS AS (`ilosc` * `szt_w_wor`) STORED,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kod` (`kod`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wydruki`
--

LOCK TABLES `wydruki` WRITE;
/*!40000 ALTER TABLE `wydruki` DISABLE KEYS */;
INSERT INTO `wydruki` VALUES (33,'HKL3D_0001__V1','Podkładki do pilotów szare 50mm',8,50,400),(34,'HKL3D_0002__V1','Podkładki dystansowe',8,50,400),(35,'HKL3D_0003__V1','narożnik',4,50,200),(36,'HKL3D_0004__V1','tulejka 6mm',7,250,1750),(61,'HKL3D_0005__V1','Podkładki do pilotów czarne 50mm',5,100,500),(62,'HKL3D_0006__V1','Podkładka dystansowa do smartcode',2,200,400),(63,'HKL3D_0007__V1','Pająk mocowania do elektryków chr łamane plisy',2,100,200),(64,'HKL3D_0008__V1','(do wyjaśnienia)',5,100,500),(65,'HKL3D_0009__V1','Podkładka dystansowa plisy (biała z śrubą)',1,60,60),(66,'HKL3D_0010__V1','Podkładka dystansowa plisy (biała bez śruby)',1,140,140),(67,'HKL3D_0011__V1','Podkładka dystansowa plisy (kremowa bez śruby)',1,100,100),(68,'HKL3D_0012__V1','??',1,95,95),(69,'HKL3D_0013__V1','??',3,400,1200),(70,'HKL3D_0014__V1','??',8,70,560),(71,'HKL3D_0015__V1','??',1,70,70),(72,'HKL3D_0016__V1','??',3,60,180),(73,'HKL3D_0017__V1','??',2,25,50),(74,'HKL3D_0018__V1','??',3,180,540),(75,'HKL3D_0019__V1','??',1,100,100),(76,'HKL3D_0020__V1','??',2,60,120),(77,'HKL3D_0021__V1','??',3,70,210),(78,'HKL3D_0022__V1','??',2,60,120),(79,'HKL3D_0023__V1','??',2,40,80),(80,'HKL3D_0024__V1','??',1,70,70),(81,'HKL3D_0025__V1','?? (kremowe)',2,16,32),(82,'HKL3D_0026__V1','??',2,20,40),(83,'HKL3D_0027__V1','??',1,16,16),(84,'HKL3D_0028__V1','??',1,30,30),(85,'HKL3D_0029__V1','??',1,40,40),(86,'HKL3D_0030__V1','??',1,100,100),(87,'HKL3D_0031__V1','??',1,9,9),(88,'HKL3D_0032__V1','??',1,18,18),(89,'HKL3D_0033__V1','??',1,65,65),(90,'HKL3D_0034__V1','??',1,13,13),(91,'HKL3D_0035__V1','??',1,7,7),(92,'HKL3D_0036__V1','??',4,140,560);
/*!40000 ALTER TABLE `wydruki` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-29  6:55:10
