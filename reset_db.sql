-- Reset Database Script for Remote Database (TiDB)
-- Run this entire script in your TiDB SQL Editor to start fresh

-- 1. Drop existing tables (to ensure clean slate)
-- Wait for users table to be dropped before creating it again
DROP TABLE IF EXISTS study_sessions;
DROP TABLE IF EXISTS users;

-- 2. Create Users Table FIRST
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Study Sessions Table SECOND (references users)
CREATE TABLE study_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    study_date DATE NOT NULL,
    subject VARCHAR(100) NOT NULL,
    hours FLOAT NOT NULL,
    difficulty ENUM('Easy','Medium','Hard') NOT NULL,
    mood ENUM('Fresh','Normal','Tired') NOT NULL,
    notes TEXT,
    productivity FLOAT,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
