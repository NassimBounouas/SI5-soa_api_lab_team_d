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
id_request integer,
id_meal varchar(255),
id_restaurant varchar(255),
client_name varchar(255),
client_address varchar(255),
command_statut varchar(255)
);

 INSERT INTO to_get_restaurant(meal_name,restaurant_name,price) VALUES ("Ramen","Lyianhg Restaurant",5);
 INSERT INTO to_get_restaurant(meal_name,restaurant_name,price) VALUES ("Pizza","Bar Roger",7);
