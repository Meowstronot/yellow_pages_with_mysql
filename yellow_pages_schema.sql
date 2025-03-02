CREATE DATABASE IF NOT EXISTS yellow_pages;
USE yellow_pages;

-- Tabel profil
CREATE TABLE IF NOT EXISTS profil (
    email VARCHAR(50) NOT NULL PRIMARY KEY,
    full_name VARCHAR(50) NOT NULL,
    nickname VARCHAR(50),
    gender ENUM('Male', 'Female') NOT NULL,
    state VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(50)
);

-- Tabel contact
CREATE TABLE IF NOT EXISTS contact (
    phone_number VARCHAR(13) NOT NULL PRIMARY KEY,
    email VARCHAR(50) NOT NULL UNIQUE, 
    facebook VARCHAR(50),
    instagram VARCHAR(50),
    twitter VARCHAR(50),
    FOREIGN KEY (email) REFERENCES profil(email) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Tabel category
CREATE TABLE IF NOT EXISTS category (
    phone_number VARCHAR(13) NOT NULL PRIMARY KEY,
    category VARCHAR(50) NOT NULL,
    notes VARCHAR(50),
    last_update DATETIME NOT NULL,
    FOREIGN KEY (phone_number) REFERENCES contact(phone_number) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS recycle_bin(
	id INT NOT NULL PRIMARY KEY,
    phone_number VARCHAR(13) NOT NULL,
    email VARCHAR(50) NOT NULL,
    full_name VARCHAR(50) NOT NULL,
    nickname VARCHAR(50),
    gender ENUM('Male', 'Female') NOT NULL,
    state VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    address VARCHAR(50),
    contact_category VARCHAR(50) NOT NULL,
    notes VARCHAR(50),
    facebook VARCHAR(50),
    instagram VARCHAR(50),
    twitter VARCHAR(50),
    last_update DATETIME NOT NULL
)