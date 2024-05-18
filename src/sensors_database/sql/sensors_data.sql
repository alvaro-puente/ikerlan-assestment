CREATE DATABASE IF NOT EXISTS sensors_database;

USE sensors_database;

CREATE TABLE sensors_data (
  id CHAR(36) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(100) NOT NULL,
  value VARCHAR(100) NOT NULL,
  timestamp DATETIME NOT NULL,
);