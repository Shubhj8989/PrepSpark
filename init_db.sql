-- Init Script for Remote Database (TiDB)
-- Run this entire script in your TiDB SQL Editor

-- 1. Create Tables
CREATE TABLE IF NOT EXISTS study_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    study_date DATE NOT NULL,
    subject VARCHAR(100) NOT NULL,
    hours FLOAT NOT NULL,
    difficulty ENUM('Easy','Medium','Hard') NOT NULL,
    mood ENUM('Fresh','Normal','Tired') NOT NULL,
    notes TEXT,
    productivity FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Add Foreign Key if not exists
-- Safe check to add column only if missing
SET @dbname = DATABASE();
SET @tablename = "study_sessions";
SET @columnname = "user_id";
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  "SELECT 1",
  "ALTER TABLE study_sessions ADD COLUMN user_id INT, ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;"
));
PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;
