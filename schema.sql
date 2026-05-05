CREATE DATABASE LocationDB;
USE LocationDB;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE Map_Search (
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    location_name VARCHAR(255) NOT NULL,
    search_time DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE Travel_Distance (
    travel_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    distance_km FLOAT NOT NULL,
    destination VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE Nearby_Places (
    place_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    place_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE Notification_History (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    notification_time DATETIME NOT NULL,
    esp32_pushed_time DATETIME DEFAULT NULL,
    app_name VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
        ON DELETE CASCADE
);