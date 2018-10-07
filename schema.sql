CREATE DATABASE ordering_db; 
USE ordering_db;

CREATE TABLE to_get_restaurant (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
restaurant_name varchar(255),
price integer
);

CREATE TABLE to_get_recipe(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
restaurant_name varchar(255),
delivery_date DATETIME,
delivery_adress varchar(255)
);

 INSERT INTO to_get_restaurant(meal_name,restaurant_name) VALUES ("Ramen","Lyianhg Restaurant");
 INSERT INTO to_get_restaurant(meal_name,restaurant_name) VALUES ("Pizza","Bar Roger");
