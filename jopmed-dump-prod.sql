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
DROP TABLE IF EXISTS users;

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

INSERT INTO users (username, email, password, first_name, last_name, created_at, updated_at) 
VALUES ('johndoe', 'johndoe@example.com', 'password123', 'John', 'Doe', NOW(), NOW()),
('janedoe', 'janedoe@example.com', 'password456', 'Jane', 'Doe', NOW(), NOW());

-- Addresses Table
DROP TABLE IF EXISTS addresses;
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

INSERT INTO addresses (user_id, city, country, zip_code, street_address, phone_number, created_at, updated_at) VALUES
(1, 'New York', 'USA', '10001', '123 Main St', '123-456-7890', NOW(), NOW()),
(2, 'Los Angeles', 'USA', '90001', '456 Elm St', '098-765-4321', NOW(), NOW());

-- Payment Information Table
DROP TABLE IF EXISTS payment_information;

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

-- Insert sample data into payment_information table
INSERT INTO payment_information (user_id, card_number, card_expiry_date, card_cvv, created_at, updated_at) VALUES
(1, '4111111111111111', '2025-12-01', '123', NOW(), NOW()),
(2, '5555555555554444', '2024-11-01', '456', NOW(), NOW());

  
-- Shipping Methods Table
DROP TABLE IF EXISTS shipping_methods;

CREATE TABLE shipping_methods (  
   id INT NOT NULL AUTO_INCREMENT,  
   name VARCHAR(255) NOT NULL,  
   description TEXT,  
   created_at DATETIME NOT NULL,  
   updated_at DATETIME NOT NULL,  
   PRIMARY KEY (id)  
);

-- Insert sample data into shipping_methods table
INSERT INTO shipping_methods (name, description, created_at, updated_at) VALUES
('Standard Shipping', 'Delivery within 5-7 business days', NOW(), NOW()),
('Express Shipping', 'Delivery within 1-2 business days', NOW(), NOW());

  
-- Shipping Information Table
DROP TABLE IF EXISTS shipping_information;

CREATE TABLE shipping_information (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_id INT NOT NULL,
    shipping_method_id INT NOT NULL,
    tracking_number VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (address_id) REFERENCES addresses(id),
    FOREIGN KEY (shipping_method_id) REFERENCES shipping_methods(id)
); 

-- Insert sample data into shipping_information table
INSERT INTO shipping_information (user_id, address_id, shipping_method_id, tracking_number, created_at, updated_at) VALUES
(1, 1, 1, 'TRACK12345', NOW(), NOW()), -- Standard Shipping for John Doe
(2, 2, 2, 'TRACK67890', NOW(), NOW()); -- Express Shipping for Jane Doe

-- Categories Table
DROP TABLE IF EXISTS categories;

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

-- Insert sample data into categories table
INSERT INTO categories (name, slug, description, created_at, updated_at) VALUES
('Medicines', 'medicines', 'Various types of medicines', NOW(), NOW()),
('Supplements', 'supplements', 'Health supplements and vitamins', NOW(), NOW());
  
-- Product Categories Table
DROP TABLE IF EXISTS product_categories;

CREATE TABLE product_categories (  
   id INT NOT NULL AUTO_INCREMENT,  
   product_id INT NOT NULL,  
   category_id INT NOT NULL,  
   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,  
   updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  
   PRIMARY KEY (id),  
   FOREIGN KEY (product_id) REFERENCES products(id),  
   FOREIGN KEY (category_id) REFERENCES categories(id)  
);

-- Insert sample data into product_categories table
INSERT INTO product_categories (product_id, category_id, created_at, updated_at) VALUES
(1, 1, NOW(), NOW()),
(2, 2, NOW(), NOW());
  
-- Products/Medicines Table
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    category VARCHAR(255),
    slug VARCHAR(255),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id)
);

-- Insert sample data into products table
INSERT INTO products (name, description, price, stock, category, slug, created_at, updated_at) VALUES
('Paracetamol', 'Pain reliever and fever reducer', 5.99, 100, 'Medicines', 'paracetamol', NOW(), NOW()),
('Vitamin C', 'Immune system booster', 10.50, 200, 'Supplements', 'vitamin-c', NOW(), NOW());

-- Product Images Table
DROP TABLE IF EXISTS product_images;

CREATE TABLE product_images (  
   id INT NOT NULL AUTO_INCREMENT,  
   product_id INT NOT NULL,  
   image_url VARCHAR(255) NOT NULL,  
   created_at DATETIME NOT NULL,  
   updated_at DATETIME NOT NULL,  
   PRIMARY KEY (id),  
   FOREIGN KEY (product_id) REFERENCES products(id)  
);

-- Insert sample data into product_images table
INSERT INTO product_images (product_id, image_url, created_at, updated_at) VALUES
(1, 'http://example.com/images/paracetamol.jpg', NOW(), NOW()),
(2, 'http://example.com/images/vitamin-c.jpg', NOW(), NOW());
  
-- Orders Table
DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_id INT NOT NULL,
    status ENUM('pending', 'shipped', 'delivered', 'cancelled') NOT NULL,
    payment_method ENUM('credit_card', 'debit_card', 'paypal', 'cash_on_delivery') NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (address_id) REFERENCES addresses(id)
); 

-- Insert sample data into orders table
INSERT INTO orders (user_id, status, payment_method, total_amount, created_at, updated_at) VALUES
(1, 'pending', 'credit_card', 15.99, NOW(), NOW()),
(2, 'completed', 'paypal', 21.00, NOW(), NOW());

-- Order Items Table
DROP TABLE IF EXISTS order_items;

CREATE TABLE order_items (
    id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample data into order_items table
INSERT INTO order_items (order_id, product_id, quantity, price, created_at, updated_at) VALUES
(1, 1, 2, 5.99, NOW(), NOW()), -- 2 Paracetamol in order 1
(2, 2, 2, 10.50, NOW(), NOW()); -- 2 Vitamin C in order 2

-- Inventory Management Table
DROP TABLE IF EXISTS inventory;

CREATE TABLE inventory (
    id INT NOT NULL AUTO_INCREMENT,
    product_id INT NOT NULL,
    supplier VARCHAR(255),
    quantity INT NOT NULL,
    restock_level INT NOT NULL,
    restock_date DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample data into inventory table
INSERT INTO inventory (product_id, supplier, quantity, restock_level, restock_date, created_at, updated_at) VALUES
(1, 'Supplier A', 100, 20, NOW(), NOW(), NOW()),
(2, 'Supplier B', 200, 30, NOW(), NOW(), NOW());

-- Payments Table
DROP TABLE IF EXISTS payments;

CREATE TABLE payments (
    id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_id VARCHAR(255),
    payment_date DATETIME NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Insert sample data into payments table
INSERT INTO payments (order_id, payment_status, amount, transaction_id, payment_date, created_at, updated_at) VALUES
(1, 'pending', 15.99, 'TXN123456', NOW(), NOW(), NOW()),
(2, 'completed', 21.00, 'TXN789012', NOW(), NOW(), NOW());

-- Reviews Table
DROP TABLE IF EXISTS reviews;

CREATE TABLE reviews (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample data into reviews table
INSERT INTO reviews (user_id, product_id, comment, rating, created_at, updated_at) VALUES
(1, 1, 'Great product, very effective!', 5, NOW(), NOW()),
(2, 2, 'Not satisfied with the quality.', 2, NOW(), NOW());
  
-- Tags Table
DROP TABLE IF EXISTS tags;

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

-- Insert sample data into tags table
INSERT INTO tags (name, slug, description, created_at, updated_at) VALUES
('Pain Relief', 'pain-relief', 'Products for pain relief', NOW(), NOW()),
('Immune Support', 'immune-support', 'Products for immune support', NOW(), NOW());

-- Products Categories Table
DROP TABLE IF EXISTS products_categories;

CREATE TABLE products_categories (
    category_id INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (category_id, product_id),
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Insert sample data into products_categories table
INSERT INTO products_categories (category_id, product_id) VALUES
(1, 1), -- Paracetamol in Medicines category
(2, 2); -- Vitamin C in Supplements category

-- Products Tags Table
DROP TABLE IF EXISTS products_tags;

CREATE TABLE products_tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    tag_id INT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);

-- Insert sample data into products_tags table
INSERT INTO products_tags (product_id, tag_id, created_at, updated_at) VALUES
(1, 1, NOW(), NOW()), -- Paracetamol tagged with Pain Relief
(2, 2, NOW(), NOW()); -- Vitamin C tagged with Immune Support
  
-- Users Roles Table - associate users with their respective roles
DROP TABLE IF EXISTS users_roles;

CREATE TABLE users_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Insert sample data into users_roles table
INSERT INTO users_roles (user_id, role_id, created_at) VALUES
(1, 1, NOW()), -- John Doe with role 1
(2, 2, NOW()); -- Jane Doe with role 2

-- Roles Table - defines the different roles available in the system
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    description VARCHAR(100),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE (name)
);

-- Insert sample data into roles table
INSERT INTO roles (name, description, created_at, updated_at) VALUES
('Admin', 'Administrator role', NOW(), NOW()),
('Customer', 'Customer role', NOW(), NOW());

-- Comments Table
DROP TABLE IF EXISTS comments;

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

-- Insert sample data into comments table
INSERT INTO comments (user_id, product_id, content, rating, created_at, updated_at) VALUES
(1, 1, 'Great product, very effective!', 5, NOW(), NOW()),
(2, 2, 'Not satisfied with the quality.', 2, NOW(), NOW());
  
-- File Uploads Table
DROP TABLE IF EXISTS file_uploads;

CREATE TABLE file_uploads (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
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
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Insert sample data into file_uploads table
INSERT INTO file_uploads (user_id, type, file_path, file_name, file_size, original_name, created_at, updated_at, tag_id, product_id, category_id) VALUES
(1, 'image', '/uploads/images/paracetamol.jpg', 'paracetamol.jpg', 1024, 'paracetamol.jpg', NOW(), NOW(), 1, 1, 1),
(2, 'image', '/uploads/images/vitamin-c.jpg', 'vitamin-c.jpg', 2048, 'vitamin-c.jpg', NOW(), NOW(), 2, 2, 2);

-- Prescription Table
DROP TABLE IF EXISTS prescriptions;

CREATE TABLE prescriptions (
    id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    doctor_id INT NOT NULL,
    prescription_date DATETIME NOT NULL,
    expiration_date DATETIME NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- Insert sample data into prescriptions table
INSERT INTO prescriptions (user_id, doctor_id, prescription_date, expiration_date) VALUES
(1, 1, NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR)),
(2, 2, NOW(), DATE_ADD(NOW(), INTERVAL 1 YEAR));

-- Doctors Table
DROP TABLE IF EXISTS doctors;

CREATE TABLE doctors (
    id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    specialization VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (email),
    UNIQUE (phone_number)
);

-- Insert sample data into doctors table
INSERT INTO doctors (first_name, last_name, specialization, email, phone_number, created_at, updated_at) VALUES
('John', 'Smith', 'Cardiology', 'john.smith@example.com', '123-456-7890', NOW(), NOW()),
('Jane', 'Doe', 'Neurology', 'jane.doe@example.com', '098-765-4321', NOW(), NOW());

-- Create Indexes
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_addresses_user_id ON addresses (user_id);
CREATE INDEX idx_shipping_methods_name ON shipping_methods (name);
CREATE INDEX idx_categories_name ON categories (name);
CREATE INDEX idx_categories_slug ON categories (slug);
CREATE INDEX idx_products_name ON products (name);
CREATE INDEX idx_products_slug ON products (slug); -- Create index on slug column
CREATE INDEX idx_products_categories_product_id ON products_categories (product_id);
CREATE INDEX idx_products_categories_category_id ON products_categories (category_id);
CREATE INDEX idx_orders_user_id ON orders (user_id);
CREATE INDEX idx_orders_address_id ON orders (address_id);
CREATE INDEX idx_order_items_order_id ON order_items (order_id);
CREATE INDEX idx_order_items_product_id ON order_items (product_id);
CREATE INDEX idx_reviews_user_id ON reviews (user_id);
CREATE INDEX idx_reviews_product_id ON reviews (product_id);
CREATE INDEX idx_tags_name ON tags (name);
CREATE INDEX idx_tags_slug ON tags (slug);
CREATE INDEX idx_products_tags_product_id ON products_tags (product_id);
CREATE INDEX idx_products_tags_tag_id ON products_tags (tag_id);
CREATE INDEX idx_roles_name ON roles (name);
CREATE INDEX idx_users_roles_user_id ON users_roles (user_id);
CREATE INDEX idx_users_roles_role_id ON users_roles (role_id);
CREATE INDEX idx_comments_user_id ON comments (user_id);
CREATE INDEX idx_comments_product_id ON comments (product_id);
CREATE INDEX idx_file_uploads_user_id ON file_uploads (user_id);
