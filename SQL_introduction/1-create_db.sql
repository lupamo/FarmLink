-- creates database fm_ln_0 if does not exist in MySQL
CREATE DATABASE IF NOT EXISTS fm_ln_0;
GRANT ALL PRIVILEGES ON fm_ln_0.* TO 'farmlink_user'@'localhost';
FLUSH PRIVILEGES;


