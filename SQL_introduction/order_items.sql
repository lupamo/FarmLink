-- creates table for order items with columns
USE fm_ln_0;

CREATE TABLE IF NOT EXISTS orderItems (
	id INT AUTO_INCREMENT PRIMARY KEY,
	orders_id INT NOT NULL,
    products_id INT NOT NULL,
	quantity INT NOT NULL,
	price DECIMAL (10, 2) NOT NULL,
	FOREIGN KEY (orders_id) REFERENCES orders(id),
	FOREIGN KEY (products_id) REFERENCES products(id)
);

-- dumps data into orderItems table
INSERT INTO orderItems (orders_id, products_id, quantity, price) VALUES
(1, 1, 10, 25);
