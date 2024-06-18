-- creates table for reviews with columns
USE fm_ln_0;

CREATE TABLE IF NOT EXISTS reviews (
	id INT AUTO_INCREMENT PRIMARY KEY,
       	products_id INT NOT NULL,
	customers_id INT NOT NULL,
	rating INT NOT NULL,
	comment TEXT,
	FOREIGN KEY (products_id) REFERENCES products(id),
	FOREIGN KEY (customers_id) REFERENCES customers(id)
);

-- dumps data into reviews table
INSERT INTO reviews (products_id, customers_id, rating,comment) VALUES
(1, 1, 9, 'I loved it');
