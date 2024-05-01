CREATE TABLE IF NOT EXISTS user (
    vd_user_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_user_name VARCHAR(255),
    vd_user_password VARCHAR(255),
    vd_user_function VARCHAR(255),
    vd_user_firstname VARCHAR(255),
    vd_user_lastname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS category (
    vd_category_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_category_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS product (
    vd_product_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_product_code VARCHAR(255),
    vd_product_name VARCHAR(255),
    vd_product_price DECIMAL(10, 2),
    vd_product_vat INT,
    vd_product_category INT,
    FOREIGN KEY (vd_product_category) REFERENCES category(vd_category_id)
);

CREATE TABLE IF NOT EXISTS inventory (
    vd_inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_inventory_vending_machine_id INT,
    vd_inventory_product_id INT,
    vd_inventory_stock_quantity INT,
    vd_inventory_min_stock INT,
    vd_inventory_max_stock INT,
    vd_inventory_refill_stock INT,
    FOREIGN KEY (vd_inventory_product_id) REFERENCES product(vd_product_id)
);

CREATE TABLE IF NOT EXISTS vending_machine (
    vd_vending_machine_ID INT AUTO_INCREMENT PRIMARY KEY,
    vd_vending_machine_location VARCHAR(255),
    vd_vending_machine_address VARCHAR(255),
    vd_vending_machine_postal_code VARCHAR(255),
    vd_vending_machine_city VARCHAR(255),
    vd_vending_machine_country VARCHAR(255),
    FOREIGN KEY (vd_vending_machine_id) REFERENCES inventory(vd_inventory_vending_machine_id),
    FOREIGN KEY (vd_vending_machine_ID) REFERENCES invoice(vd_invoice_vending_machine_id)
);

CREATE TABLE IF NOT EXISTS supplier (
    vd_supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_supplier_product_id INT,
    vd_supplier_name VARCHAR(255),
    vd_supplier_address VARCHAR(255),
    vd_supplier_postal_code VARCHAR(20),
    vd_supplier_city VARCHAR(255),
    vd_supplier_country VARCHAR(255),
    vd_supplier_phone_number VARCHAR(20),
    vd_supplier_email VARCHAR(255),
    FOREIGN KEY (vd_supplier_product_id) REFERENCES product(vd_product_id)
);

CREATE TABLE IF NOT EXISTS invoice (
    vd_invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_invoice_vending_machine_id INT,
    vd_invoice_product_id INT,
    vd_invoice_date DATE,
    vd_invoice_time TIME,
    vd_invoice_payment_id INT,
    FOREIGN KEY (vd_invoice_product_id) REFERENCES product(vd_product_id),
    FOREIGN KEY (vd_invoice_payment_id) REFERENCES payment(vd_payment_id)
);

CREATE TABLE IF NOT EXISTS payment (
    vd_payment_id INT AUTO_INCREMENT PRIMARY KEY,
    vd_payment_method VARCHAR(10)
);