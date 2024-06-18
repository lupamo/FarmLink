-- creates first table farmers if it does not exist plus rows
USE fm_ln_0;
CREATE TABLE IF NOT EXISTS farmers (
	id INT AUTO_INCREMENT PRIMARY KEY, 
	name VARCHAR(256) NOT NULL,
	contact VARCHAR(255),
	location VARCHAR(255)
);

-- dump data into the farmers table
INSERT INTO farmers (name, contact, location) VALUES ('Miles Richards', '0701175232', 'Muranga');
INSERT INTO farmers (name, contact, location) VALUES ('Mwangi Paul', '0705675232', 'Kiambu');
INSERT INTO farmers (name, contact, location) VALUES ('Miles Richars', '0703175282', 'Mwingi');
