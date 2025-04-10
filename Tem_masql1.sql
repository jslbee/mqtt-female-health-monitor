-- Create database
CREATE DATABASE sql_tutorial1;
USE sql_tutorial1;

-- Create user table
CREATE TABLE IF NOT EXISTS user (
    user_ID INT PRIMARY KEY
);

-- Create temperature sensor table
CREATE TABLE temperature_sensor (
    temperatureSensor_ID INT AUTO_INCREMENT PRIMARY KEY,
    user_ID INT NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    record_time DATETIME NOT NULL,
    FOREIGN KEY (user_ID) REFERENCES user(user_ID)
);

-- Insert data into the user table
INSERT INTO user (user_ID) VALUES (1), (2), (3), (4), (5), (6), (7), (8);

-- Insert data into the temperature_sensor table
INSERT INTO temperature_sensor (user_ID, temperature, record_time) VALUES
(1, 36.5, '2025-04-02 08:00:00'),
(1, 36.7, '2025-04-02 09:00:00'),
(2, 37.0, '2025-04-02 10:00:00'),
(2, 36.9, '2025-04-02 11:00:00'),
(3, 36.8, '2025-04-02 12:00:00'),
(3, 36.6, '2025-04-02 13:00:00'),
(4, 37.1, '2025-04-02 14:00:00'),
(4, 36.5, '2025-04-02 15:00:00'),
(5, 36.7, '2025-04-02 16:0000:'),
(5, 36.9, '2025-04-02 17:00:00'),
(6, 36.8, '2025-04-02 18:00:00'),
(6, 36.6, '2025-04-02 19:00:00'),
(7, 37.1, '2025-04-02 20:00:00');

-- View the structure of the temperature_
DESCRIBE temperature_sensor;

SELECT * FROM temperature_sensor;
