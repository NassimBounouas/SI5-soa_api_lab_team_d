CREATE DATABASE test_db; 
USE test_db;
CREATE TABLE test_table (
`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
test_name varchar(255) 
);

INSERT INTO test_table (test_name) VALUES ("test_entry");
