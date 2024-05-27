'inventory', ('CREATE TABLE `inventory` '
              '(\n  `vd_inventory_id` int NOT NULL AUTO_INCREMENT,'
              '\n  `vd_inventory_vending_machine_id` int DEFAULT NULL,'
              '\n  `vd_inventory_product_id` int DEFAULT NULL,'
              '\n  `vd_inventory_stock_quantity` int DEFAULT NULL,'
              '\n  `vd_inventory_min_stock` int DEFAULT NULL,'
              '\n  `vd_inventory_max_stock` int DEFAULT NULL,'
              '\n  `vd_inventory_refill_stock` int DEFAULT NULL,'
              '\n  PRIMARY KEY (`vd_inventory_id`),'
              '\n  KEY `inventory_ibfk_1_idx` (`vd_inventory_product_id`),'
              '\n  KEY `idx_inventory_vending_machine_id` (`vd_inventory_vending_machine_id`),'
              '\n  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`vd_inventory_product_id`) REFERENCES `product` (`vd_product_id`),'
              '\n  CONSTRAINT `inventory_ibfk_2` FOREIGN KEY (`vd_inventory_vending_machine_id`) REFERENCES `vending_machine` (`vd_vending_machine_ID`)'
              '\n) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')


# Table, Create Table
'category', ('CREATE TABLE `category` '
             '(\n  `vd_category_id` int NOT NULL AUTO_INCREMENT,'
             '\n  `vd_category_name` varchar(255) DEFAULT NULL,'
             '\n  PRIMARY KEY (`vd_category_id`)'
             '\n) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')


# Table, Create Table
'user', ('CREATE TABLE `user` '
         '(\n  `vd_user_id` int NOT NULL AUTO_INCREMENT,'
         '\n  `vd_user_name` varchar(255) DEFAULT NULL,'
         '\n  `vd_user_password` varchar(255) DEFAULT NULL,'
         '\n  `vd_user_function` varchar(255) DEFAULT NULL,'
         '\n  `vd_user_firstname` varchar(255) DEFAULT NULL,'
         '\n  `vd_user_lastname` varchar(255) DEFAULT NULL,'
         '\n  PRIMARY KEY (`vd_user_id`)\n) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')


# Table, Create Table
'product', ('CREATE TABLE `product` ('
            '\n  `vd_product_id` int NOT NULL AUTO_INCREMENT,'
            '\n  `vd_product_code` varchar(255) DEFAULT NULL,'
            '\n  `vd_product_name` varchar(255) DEFAULT NULL,'
            '\n  `vd_product_price` decimal(10,2) DEFAULT NULL,'
            '\n  `vd_product_vat` int DEFAULT NULL,'
            '\n  `vd_product_category` varchar(255) DEFAULT NULL,'
            '\n  PRIMARY KEY (`vd_product_id`),'
            '\n  KEY `vd_product_category` (`vd_product_category`)'
            '\n) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')


# Table, Create Table
'vending_machine', ('CREATE TABLE `vending_machine` ('
                    '\n  `vd_vending_machine_ID` int NOT NULL AUTO_INCREMENT,'
                    '\n  `vd_vending_machine_location` varchar(255) DEFAULT NULL,'
                    '\n  `vd_vending_machine_address` varchar(255) DEFAULT NULL,'
                    '\n  `vd_vending_machine_postal_code` varchar(255) DEFAULT NULL,'
                    '\n  `vd_vending_machine_city` varchar(255) DEFAULT NULL,'
                    '\n  `vd_vending_machine_country` varchar(255) DEFAULT NULL,'
                    '\n  PRIMARY KEY (`vd_vending_machine_ID`)\n) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')


# Table, Create Table
'supplier', ('CREATE TABLE `supplier` ('
             '\n  `vd_supplier_id` int NOT NULL AUTO_INCREMENT,'
             '\n  `vd_supplier_product_id` int DEFAULT NULL,'
             '\n  `vd_supplier_name` varchar(255) DEFAULT NULL,'
             '\n  `vd_supplier_address` varchar(255) DEFAULT NULL,'
             '\n  `vd_supplier_postal_code` varchar(20) DEFAULT NULL,'
             '\n  `vd_supplier_city` varchar(255) DEFAULT NULL,'
             '\n  `vd_supplier_country` varchar(255) DEFAULT NULL,'
             '\n  `vd_supplier_phone_number` varchar(20) DEFAULT NULL,'
             '\n  `vd_supplier_email` varchar(255) DEFAULT NULL,'
             '\n  PRIMARY KEY (`vd_supplier_id`),\n  KEY `vd_supplier_product_id` (`vd_supplier_product_id`),'
             '\n  CONSTRAINT `supplier_ibfk_1` FOREIGN KEY (`vd_supplier_product_id`) REFERENCES `product` (`vd_product_id`)\n) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')

# Table, Create Table
'invoice', ('CREATE TABLE `invoice` ('
            '\n  `vd_invoice_id` int NOT NULL AUTO_INCREMENT,'
            '\n  `vd_invoice_vending_machine_id` int DEFAULT NULL,'
            '\n  `vd_invoice_product_id` int DEFAULT NULL,'
            '\n  `vd_invoice_date` date DEFAULT NULL,'
            '\n  `vd_invoice_time` time DEFAULT NULL,'
            '\n  `vd_invoice_payment_id` int DEFAULT NULL,'
            '\n  PRIMARY KEY (`vd_invoice_id`),'
            '\n  KEY `vd_invoice_product_id` (`vd_invoice_product_id`),'
            '\n  KEY `vd_invoice_payment_id` (`vd_invoice_payment_id`),'
            '\n  KEY `idx_vending_machine_id` (`vd_invoice_vending_machine_id`),'
            '\n  CONSTRAINT `invoice_ibfk_1` FOREIGN KEY (`vd_invoice_product_id`) REFERENCES `product` (`vd_product_id`),'
            '\n  CONSTRAINT `invoice_ibfk_2` FOREIGN KEY (`vd_invoice_payment_id`) REFERENCES `payment` (`vd_payment_id`),'
            '\n  CONSTRAINT `invoice_ibfk_3` FOREIGN KEY (`vd_invoice_vending_machine_id`) REFERENCES `vending_machine` (`vd_vending_machine_ID`)\n) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')

'payment', ('CREATE TABLE `payment` ('
            '\n  `vd_payment_id` int NOT NULL AUTO_INCREMENT,'
            '\n  `vd_payment_method` varchar(10) DEFAULT NULL,'
            '\n  PRIMARY KEY (`vd_payment_id`)\n) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')
