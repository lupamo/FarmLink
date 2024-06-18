-- creates table for orders with columns
USE fm_ln_0;

CREATE TABLE IF NOT EXISTS orders (
	id INT AUTO_INCREMENT PRIMARY KEY,
       	customers_id INT NOT NULL,
	subtotal INT(255) NOT NULL,
	FOREIGN KEY (customers_id) REFERENCES customers(id)
);

-- dumps data into orders table
INSERT INTO orders (customers_id, subtotal) VALUES
(1, 10);
