-- creates first table customers if it does not exist plus rows
USE fm_ln_0;
CREATE TABLE IF NOT EXISTS customers (
	id INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(256) NOT NULL,
	contact VARCHAR(255),
	address VARCHAR(255)
);

-- dump data into the customers table
INSERT INTO customers (name, contact, address) VALUES ('Lori Iman', '0701546544', 'Muranga');
INSERT INTO customers (name, contact, address) VALUES ('Khalif Kairo', '0704567332', 'Kiambu');
INSERT INTO customers (name, contact, address) VALUES ('Flora Limki', '0706547382', 'Mwingi');
