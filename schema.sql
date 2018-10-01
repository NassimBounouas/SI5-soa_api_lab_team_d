CREATE DATABASE delivery_db; 
USE delivery_db;

CREATE TABLE to_deliver_table (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
meal_name varchar(255),
pickup_address varchar(255),
delivery_address varchar(255)
);

INSERT INTO to_deliver_table (meal_name, pickup_address, delivery_address) VALUES ("test_meal", "test_pickup", "test_delivery");
