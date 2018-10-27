/* SCHEMA FOR MENU SERVICE */
/* @author: Nikita ROUSSEAU */
/* @updated: 27/10/2018 */

CREATE DATABASE  IF NOT EXISTS `soa`;
USE `soa`;

-- Host: localhost    Database: soa
-- ------------------------------------------------------
-- Server version	5.7.14

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `idcategory` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `region` varchar(255) DEFAULT NULL,
  `image` text,
  PRIMARY KEY (`idcategory`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Table structure for table `meal`
--

DROP TABLE IF EXISTS `meal`;
CREATE TABLE `meal` (
  `idmeal` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `idcategory` int(10) unsigned NOT NULL,
  `idrestaurant` int(10) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `price` float unsigned DEFAULT '0',
  `is_menu` int(10) unsigned DEFAULT '0',
  `image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idmeal`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=latin1;

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
