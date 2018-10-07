CREATE DATABASE ordering_db; 
USE ordering_db;

CREATE TABLE to_get_restaurant (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
restaurant_name varchar(255)
);

CREATE TABLE to_get_recipe(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
restaurant_name varchar(255),
delivery_date integer,
delivery_adress varchar(255)
);
