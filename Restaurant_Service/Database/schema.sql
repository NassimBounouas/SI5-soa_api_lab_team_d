/* SCHEMA FOR MENU SERVICE */
/* @author: Nikita ROUSSEAU */
/* @updated: 27/10/2018 */

CREATE DATABASE  IF NOT EXISTS `soa`;
USE `soa`;

-- Host: localhost    Database: soa
-- ------------------------------------------------------
-- Server version	5.7.14

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
CREATE TABLE `restaurant` (
  `idrestaurant` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`idrestaurant`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

-- Dump completed
