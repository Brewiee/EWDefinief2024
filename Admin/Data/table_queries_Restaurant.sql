CREATE TABLE IF NOT EXISTS customer (
    rs_customer_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_customer_name VARCHAR(255),
    rs_customer_email VARCHAR(255),
    rs_customer_address VARCHAR(255),
    rs_customer_postal_code VARCHAR(20),
    rs_customer_city VARCHAR(255),
    rs_customer_country VARCHAR(255),
    rs_customer_phone_number VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS user (
    rs_user_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_user_name VARCHAR(255),
    rs_user_password VARCHAR(255),
    rs_user_function VARCHAR(255),
    rs_user_firstname VARCHAR(255),
    rs_user_lastname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS product (
    rs_product_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_product_code VARCHAR(255),
    rs_product_name VARCHAR(255),
    rs_product_price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS `table` (
    rs_table_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_table_amount_space INT,
    rs_table_reservation_id INT,
    INDEX (rs_table_reservation_id) -- Adding index to the referenced column
);

CREATE TABLE IF NOT EXISTS menu (
    rs_menu_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_menu_category VARCHAR(255),
    rs_menu_name VARCHAR(255),
    rs_menu_description TEXT,
    rs_menu_price DECIMAL(10, 2)
);

CREATE TABLE IF NOT EXISTS inventory (
    rs_inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_inventory_product_id INT,
    rs_inventory_stock_quantity INT,
    rs_inventory_min_stock INT,
    rs_inventory_max_stock INT,
    FOREIGN KEY (rs_inventory_product_id) REFERENCES product(rs_product_id)
);

CREATE TABLE IF NOT EXISTS supplier (
    rs_supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_supplier_product_id INT,
    rs_supplier_name VARCHAR(255),
    rs_supplier_address VARCHAR(255),
    rs_supplier_postal_code VARCHAR(20),
    rs_supplier_city VARCHAR(255),
    rs_supplier_country VARCHAR(255),
    rs_supplier_phone_number VARCHAR(20),
    rs_supplier_email VARCHAR(255),
    FOREIGN KEY (rs_supplier_product_id) REFERENCES product(rs_product_id)
);

CREATE TABLE IF NOT EXISTS invoice (
    rs_invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_invoice_customer_id INT,
    rs_invoice_user_id INT,
    FOREIGN KEY (rs_invoice_customer_id) REFERENCES customer(rs_customer_id),
    FOREIGN KEY (rs_invoice_user_id) REFERENCES user(rs_user_id)
);

CREATE TABLE IF NOT EXISTS invoice_line (
    rs_invoice_line_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_invoice_line_invoice_id INT,
    rs_invoice_line_product_id INT,
    rs_invoice_line_order_line_quantity INT,
    FOREIGN KEY (rs_invoice_line_invoice_id) REFERENCES invoice(rs_invoice_id),
    FOREIGN KEY (rs_invoice_line_product_id) REFERENCES product(rs_product_id)
);

CREATE TABLE IF NOT EXISTS reservation (
    rs_reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_reservation_customer_id INT,
    rs_reservation_amount INT,
    rs_reservation_time TIME,
    rs_reservation_day DATE,
    rs_reservation_table_id INT, -- New column
    FOREIGN KEY (rs_reservation_customer_id) REFERENCES customer(rs_customer_id),
    FOREIGN KEY (rs_reservation_table_id) REFERENCES `table`(rs_table_id)
);

CREATE TABLE IF NOT EXISTS `order` (
    rs_order_id INT AUTO_INCREMENT PRIMARY KEY,
    rs_order_table_id INT,
    rs_order_date DATE,
    rs_order_time TIME,
    rs_order_customer_id INT,
    rs_order_amount_people INT,
    rs_order_menu_id INT,
    FOREIGN KEY (rs_order_table_id) REFERENCES `table`(rs_table_id),
    FOREIGN KEY (rs_order_customer_id) REFERENCES customer(rs_customer_id),
    FOREIGN KEY (rs_order_menu_id) REFERENCES menu(rs_menu_id)
);
