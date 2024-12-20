-- Create database
CREATE DATABASE IF NOT EXISTS form_data;

-- Use the database
USE form_data;

-- Create form_submissions table
CREATE TABLE IF NOT EXISTS form_submissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME NOT NULL
);