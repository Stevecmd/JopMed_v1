-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: jopmed_dev_db
-- ------------------------------------------------------
-- Server version	5.7.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Warning- This is a simple dump file, it is not updated.
-- It is recommended to use the latest version of the database schema ie prod.

-- Drop database
DROP DATABASE IF EXISTS jopmed_dev_db;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS jopmed_dev_db;
CREATE USER IF NOT EXISTS 'jopmed_dev'@'localhost';
SET PASSWORD FOR 'jopmed_dev'@'localhost' = 'jopmed_dev_pwd';
GRANT ALL ON jopmed_dev_db.* TO 'jopmed_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'jopmed_dev'@'localhost';
FLUSH PRIVILEGES;

USE jopmed_dev_db;

-- Users Table
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) NOT NULL,
    email VARCHAR(120) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(300) NOT NULL,
    last_name VARCHAR(300) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (username)
);

-- Addresses Table
CREATE TABLE addresses (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    city VARCHAR(255) NOT NULL,
    country VARCHAR(255) NOT NULL,
    zip_code VARCHAR(255) NOT NULL,
    street_address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Payment Information Table
CREATE TABLE payment_information (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    card_number VARCHAR(16) NOT NULL,
    card_expiry_date DATE NOT NULL,
    card_cvv VARCHAR(3) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Shipping Information Table
CREATE TABLE shipping_information (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_id INT NOT NULL,
    shipping_method VARCHAR(255) NOT NULL,
    tracking_number VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);

-- Categories Table
CREATE TABLE categories (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY (id),
    UNIQUE (slug)
);

-- Products Table
CREATE TABLE products (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price INT NOT NULL,
    stock INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    publish_on DATETIME,
    PRIMARY KEY (id),
    UNIQUE (slug)
);

-- Orders Table
CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_id INT NOT NULL,
    order_status INT NOT NULL,
    tracking_number VARCHAR(255),
    created_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);

-- Order Items Table
CREATE TABLE order_items (
    id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    price INT NOT NULL,
    quantity INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Reviews Table
CREATE TABLE reviews (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    content TEXT NOT NULL,
    rating INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Tags Table
CREATE TABLE tags (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY (id),
    UNIQUE (slug)
);

-- Products Categories Table
CREATE TABLE products_categories (
    category_id INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (category_id, product_id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Products Tags Table
CREATE TABLE products_tags (
    product_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (product_id, tag_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

-- Users Roles Table
CREATE TABLE users_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Roles Table
CREATE TABLE roles (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    description VARCHAR(100),
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- Comments Table
CREATE TABLE comments (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    content TEXT NOT NULL,
    rating INT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- File Uploads Table
CREATE TABLE file_uploads (
    id INT NOT NULL AUTO_INCREMENT,
    type VARCHAR(15),
    file_path VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    tag_id INT,
    product_id INT,
    category_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);