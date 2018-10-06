CREATE DATABASE chinese_restaurant_db; 
USE chinese_restaurant_db;

CREATE TABLE to_prepare_table (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
order_time DATETIME,
pickup_date DATETIME,
client varchar(255),
meal_name varchar(255)
);

-- INSERT INTO to_prepare_table (order_time, meal_name) VALUES ("2018-10-06T23:58:29+02:00", "test_meal");
