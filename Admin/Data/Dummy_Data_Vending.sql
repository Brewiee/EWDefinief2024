-- Dummy data for vending_machine table
INSERT INTO vending_machine (vd_vending_machine_location, vd_vending_machine_address, vd_vending_machine_postal_code, vd_vending_machine_city, vd_vending_machine_country) VALUES ('Location 1', 'Address 1', '12345', 'City 1', 'Country 1');
INSERT INTO vending_machine (vd_vending_machine_location, vd_vending_machine_address, vd_vending_machine_postal_code, vd_vending_machine_city, vd_vending_machine_country) VALUES ('Location 2', 'Address 2', '54321', 'City 2', 'Country 2');
INSERT INTO vending_machine (vd_vending_machine_location, vd_vending_machine_address, vd_vending_machine_postal_code, vd_vending_machine_city, vd_vending_machine_country) VALUES ('Location 3', 'Address 3', '67890', 'City 3', 'Country 3');

-- Dummy data for category table
INSERT INTO category (vd_category_name) VALUES ('Category 1');
INSERT INTO category (vd_category_name) VALUES ('Category 2');
INSERT INTO category (vd_category_name) VALUES ('Category 3');

-- Dummy data for product table
INSERT INTO product (vd_product_code, vd_product_name, vd_product_price, vd_product_vat, vd_product_category) VALUES ('P001', 'Product 1', 10.00, 20, 1);
INSERT INTO product (vd_product_code, vd_product_name, vd_product_price, vd_product_vat, vd_product_category) VALUES ('P002', 'Product 2', 15.00, 20, 2);
INSERT INTO product (vd_product_code, vd_product_name, vd_product_price, vd_product_vat, vd_product_category) VALUES ('P003', 'Product 3', 20.00, 20, 3);

-- Dummy data for payment table
INSERT INTO payment (vd_payment_method) VALUES ('Cash');
INSERT INTO payment (vd_payment_method) VALUES('Credit Card');
INSERT INTO payment (vd_payment_method) VALUES('Debit Card');

-- Dummy data for supplier table
INSERT INTO supplier (vd_supplier_product_id, vd_supplier_name, vd_supplier_address, vd_supplier_postal_code, vd_supplier_city, vd_supplier_country, vd_supplier_phone_number, vd_supplier_email) VALUES (1, 'Supplier 1', 'Address 1', '12345', 'City 1', 'Country 1', '1234567890', 'supplier1@example.com');
INSERT INTO supplier (vd_supplier_product_id, vd_supplier_name, vd_supplier_address, vd_supplier_postal_code, vd_supplier_city, vd_supplier_country, vd_supplier_phone_number, vd_supplier_email) VALUES (2, 'Supplier 2', 'Address 2', '54321', 'City 2', 'Country 2', '0987654321', 'supplier2@example.com');
INSERT INTO supplier (vd_supplier_product_id, vd_supplier_name, vd_supplier_address, vd_supplier_postal_code, vd_supplier_city, vd_supplier_country, vd_supplier_phone_number, vd_supplier_email) VALUES (3, 'Supplier 3', 'Address 3', '67890', 'City 3', 'Country 3', '1112223333', 'supplier3@example.com');

-- Dummy data for inventory table
INSERT INTO inventory (vd_inventory_vending_machine_id, vd_inventory_product_id, vd_inventory_stock_quantity, vd_inventory_min_stock, vd_inventory_max_stock, vd_inventory_refill_stock) VALUES (1, 1, 50, 10, 100, 20);
INSERT INTO inventory (vd_inventory_vending_machine_id, vd_inventory_product_id, vd_inventory_stock_quantity, vd_inventory_min_stock, vd_inventory_max_stock, vd_inventory_refill_stock) VALUES (2, 2, 30, 5, 50, 10);
INSERT INTO inventory (vd_inventory_vending_machine_id, vd_inventory_product_id, vd_inventory_stock_quantity, vd_inventory_min_stock, vd_inventory_max_stock, vd_inventory_refill_stock) VALUES (3, 3, 20, 5, 30, 10);

-- Dummy data for invoice table
INSERT INTO invoice (vd_invoice_vending_machine_id, vd_invoice_product_id, vd_invoice_date, vd_invoice_time, vd_invoice_payment_id) VALUES (1, 1, '2024-05-06', '12:00:00', 1);
INSERT INTO invoice (vd_invoice_vending_machine_id, vd_invoice_product_id, vd_invoice_date, vd_invoice_time, vd_invoice_payment_id) VALUES (2, 2, '2024-05-06', '13:00:00', 2);
INSERT INTO invoice (vd_invoice_vending_machine_id, vd_invoice_product_id, vd_invoice_date, vd_invoice_time, vd_invoice_payment_id) VALUES (3, 3, '2024-05-06', '14:00:00', 3);
