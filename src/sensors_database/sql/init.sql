CREATE DATABASE IF NOT EXISTS sensors_database;

USE sensors_database;

CREATE TABLE sensors_data (
  id CHAR(36) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100) NOT NULL,
  value VARCHAR(100) NOT NULL,
  timestamp DATETIME NOT NULL,
);

CREATE DATABASE IF NOT EXISTS processed_sensors;

USE processed_sensors;

CREATE TABLE processed_data (
  id CHAR(36) PRIMARY KEY,
  value VARCHAR(100) NOT NULL,
);