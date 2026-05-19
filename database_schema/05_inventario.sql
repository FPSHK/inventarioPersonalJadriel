DROP DATABASE IF EXISTS inventario_personal;
CREATE DATABASE inventario_personal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventario_personal;

CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE item (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL,
    precio_estimado DECIMAL(10, 2),
    ubicacion VARCHAR(100),
    fecha_adquisicion DATE,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user(id)
);

INSERT INTO role (name) VALUES ('Admin'), ('Usuario'), ('Owner');
