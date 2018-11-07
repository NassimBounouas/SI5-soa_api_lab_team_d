CREATE DATABASE delivery_db; 
USE delivery_db;

CREATE TABLE to_deliver_table (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
pickup_restaurant varchar(255),
pickup_date DATETIME,
delivery_address varchar(255),
status varchar(255),
id_steed int
);

CREATE TABLE steed_database(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name varchar(255),
averagePay int,
averageTime int,
numberOfDelivery int,
longitude int,
latitude int,
lastUpdate DATETIME
);

INSERT INTO `steed_database` (name,averagePay,averageTime,numberOfDelivery,longitude,latitude,lastUpdate) VALUES ("Jamie",14,8,15,22,-40,"2018-11-07 16:00");
