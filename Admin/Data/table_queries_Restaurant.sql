-- Create table for menu items
CREATE TABLE IF NOT EXISTS menu_items (
    rs_item_id INT PRIMARY KEY AUTO_INCREMENT,
    rs_name VARCHAR(255),
    rs_description TEXT,
    rs_price DECIMAL(10,2),
    rs_category VARCHAR(255)
);

-- Create table for tables
CREATE TABLE IF NOT EXISTS tables (
    rs_table_id INT PRIMARY KEY ,
    rs_number INT ,
    rs_seats INT,
    rs_status ENUM('available', 'occupied', 'reserved', 'locked')
);

-- Create table for orders
CREATE TABLE IF NOT EXISTS orders (
    rs_order_id INT PRIMARY KEY AUTO_INCREMENT,
    rs_user_id INT,
    rs_table_number INT,
    rs_order_time DATETIME,
    rs_status ENUM('placed', 'prepared', 'served', 'paid'),
    FOREIGN KEY (rs_user_id) REFERENCES users.userinfo(user_id),
    FOREIGN KEY (rs_table_number) REFERENCES tables(rs_table_id)
);

-- Create table for order details
CREATE TABLE IF NOT EXISTS orderdetails (
    rs_order_detail_id INT PRIMARY KEY AUTO_INCREMENT,
    rs_order_id INT,
    rs_item_id INT,
    rs_quantity INT,
    rs_subtotal DECIMAL(10,2),
    FOREIGN KEY (rs_order_id) REFERENCES orders(rs_order_id),
    FOREIGN KEY (rs_item_id) REFERENCES menu_items(rs_item_id)
);

-- Create table for customers
CREATE TABLE IF NOT EXISTS customer (
    rs_customer_id INT PRIMARY KEY AUTO_INCREMENT,
    rs_name VARCHAR(100),
    rs_address VARCHAR(255),
    rs_email VARCHAR(100),
    rs_phone_number VARCHAR(20)
);

-- Create table for reservations
CREATE TABLE IF NOT EXISTS reservation (
    rs_reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    rs_customer_id INT,
    rs_reservation_date DATE,
    rs_reservation_time TIME,
    rs_party_size INT,
    rs_table_id INT,
    FOREIGN KEY (rs_customer_id) REFERENCES customer(rs_customer_id),
    FOREIGN KEY (rs_table_id) REFERENCES tables(rs_table_id)
);
