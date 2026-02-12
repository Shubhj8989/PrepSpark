CREATE DATABASE IF NOT EXISTS smart_study_analyzer;

USE smart_study_analyzer;

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
