CREATE DATABASE Lumosdb;

USE Lumosdb;

CREATE TABLE ContactForm (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    message TEXT
);

CREATE TABLE Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    review TEXT
);

ALTER TABLE Reviews CHANGE username name VARCHAR(255);

SELECT * FROM ContactForm;
SELECT * FROM Reviews;