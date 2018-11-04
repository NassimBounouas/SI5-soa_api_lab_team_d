/* SCHEMA FOR ORDERING SERVICE */
/* @author: Nikita ROUSSEAU */
/* @updated: 04/11/2018 */

CREATE DATABASE  IF NOT EXISTS `soa`;
USE `soa`;

-- Host: localhost    Database: soa
-- ------------------------------------------------------
-- Server version	5.7.14

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
CREATE TABLE `order` (
  `id_order` int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  id_meal int(10) unsigned NOT NULL,
  id_restaurant int(10) unsigned NOT NULL,
  id_code int(10) unsigned,
  client_name varchar(255),
  client_address varchar(255),
  status varchar(255)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Dump completed
