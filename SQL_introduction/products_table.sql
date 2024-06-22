-- creates table products with columns
USE fm_ln_0;

CREATE TABLE IF NOT EXISTS products (
	id INT AUTO_INCREMENT PRIMARY KEY,
    farmers_id INT NOT NULL,
	name VARCHAR(100) NOT NULL,
	description TEXT,
	price DECIMAL(10, 2) NOT NULL,
	quantityAvailable INT NOT NULL,
	FOREIGN KEY (farmers_id) REFERENCES farmers(id)
);

-- dumps data into products table
INSERT INTO products (farmers_id, Name, Description, Price, QuantityAvailable) VALUES
(1, 'Tomatoes', 'Fresh organic tomatoes', 2.50, 100);
