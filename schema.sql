CREATE DATABASE ordering_db; 
USE ordering_db;

CREATE TABLE to_get_restaurant (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255)
);

CREATE TABLE to_get_recipe(
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
restaurant_name varchar(255),
pickup_address varchar(255),
delivery_adress varchar(255)
);

INSERT INTO to_get_restaurant (meal_name) VALUES ("test_meal");
INSERT INTO to_get_recipe (meal_name,restaurant_name,pickup_address,delivery_address) VALUES ("test_meal",test_restaurant","test_pickup","test_delivery");
