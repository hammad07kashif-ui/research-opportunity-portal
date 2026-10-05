CREATE DATABASE IF NOT EXISTS research_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE research_portal;
CREATE TABLE IF NOT EXISTS opportunities (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    research_area VARCHAR(100) NOT NULL,
    faculty_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    required_skills VARCHAR(1000) NOT NULL,
    available_positions INT NOT NULL,
    application_deadline DATE NOT NULL,
    status ENUM('Open', 'Closed') NOT NULL DEFAULT 'Open',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT positive_positions CHECK (available_positions >= 1 AND available_positions <= 10000)
) ENGINE=InnoDB;
