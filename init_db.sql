-- Init Script for Remote Database (TiDB)
-- Run this entire script in your TiDB SQL Editor

-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Study Sessions Table with Foreign Key
CREATE TABLE IF NOT EXISTS study_sessions (
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
