-- Dummy data for PostalCode table
INSERT INTO PostalCode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES(3600, 'GENK');
INSERT INTO PostalCode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES(3500, 'HASSELT');
INSERT INTO PostalCode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES(3630, 'MAASMECHELEN');
INSERT INTO PostalCode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES(3530, 'HOUTHALEN-HELCHTEREN');
INSERT INTO PostalCode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES(2000, 'ANTWERPEN');
INSERT INTO PostalCode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES(1000, 'BRUSSEL');

-- Dummy data for Category table
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(1, 'Smartphones');
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(2, 'Tablets');
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(3, 'Laptops');
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(4, 'Accessory');
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(5, 'Simcards');
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(6, 'Shop/Office Supplies/Costs');
INSERT INTO Category (CR_Category_Category_ID, CR_Category_Name) VALUES(7, 'Televisions');

-- Dummy data for Supplier table
INSERT INTO Supplier (CR_Supplier_Supplier_ID, CR_Supplier_Name, CR_Supplier_Country, CR_Supplier_Address, CR_Supplier_Zipcode, CR_Supplier_City, CR_Supplier_Phone_number, CR_Supplier_Email, CR_Supplier_VAT) VALUES(1, 'ABC Electronics', 'Belgium', '123 Tech St', 3600, 'GENK', '555-123-7890', 'info@abc-electronics.com', 'VAT123ABC');
INSERT INTO Supplier (CR_Supplier_Supplier_ID, CR_Supplier_Name, CR_Supplier_Country, CR_Supplier_Address, CR_Supplier_Zipcode, CR_Supplier_City, CR_Supplier_Phone_number, CR_Supplier_Email, CR_Supplier_VAT) VALUES(2, 'XYZ Parts', 'Belgium', '456 Industrial Blvd', 3500, 'HASSELT', '777-456-2345', 'sales@xyz-parts.com', 'VAT456XYZ');
INSERT INTO Supplier (CR_Supplier_Supplier_ID, CR_Supplier_Name, CR_Supplier_Country, CR_Supplier_Address, CR_Supplier_Zipcode, CR_Supplier_City, CR_Supplier_Phone_number, CR_Supplier_Email, CR_Supplier_VAT) VALUES(3, 'GHI Materials', 'Belgium', '789 Supply Ave', 3600, 'GENK', '888-789-5678', 'info@ghi-materials.com', 'VAT789GHI');
INSERT INTO Supplier (CR_Supplier_Supplier_ID, CR_Supplier_Name, CR_Supplier_Country, CR_Supplier_Address, CR_Supplier_Zipcode, CR_Supplier_City, CR_Supplier_Phone_number, CR_Supplier_Email, CR_Supplier_VAT) VALUES(4, 'LMN Supplies', 'Belgium', '321 Resource Ln', 2000, 'ANTWERPEN', '999-234-8901', 'sales@lmn-supplies.com', 'VAT234LMN');
INSERT INTO Supplier (CR_Supplier_Supplier_ID, CR_Supplier_Name, CR_Supplier_Country, CR_Supplier_Address, CR_Supplier_Zipcode, CR_Supplier_City, CR_Supplier_Phone_number, CR_Supplier_Email, CR_Supplier_VAT) VALUES(5, 'PQR Solutions', 'Belgium', '567 Tech Plaza', 1000, 'BRUSSEL', '111-567-1234', 'info@pqr-solutions.com', 'VAT567PQR');

-- Dummy data for Product table
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(1, 'PROD001', 'Smartphone X', 500.00, 699.00, 55, 10, 65, 1, 1);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(2, 'PROD007', 'Tablet X', 150.00, 199.00, 30, 10, 50, 1, 2);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(3, 'PROD002', 'Laptop Pro', 1200.00, 1599.00, 30, 10, 40, 1, 3);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(4, 'PROD004', 'Smartphone cases', 20.00, 35.00, 400, 150, 500, 1, 4);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(5, 'PROD005', 'Base Starters-pack', 7.50, 15.00, 150, 50, 200, 4, 5);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(6, 'PROD006', 'Printing paper (100 sheets)', 35.00, 0.00, 10, 5, 16, 3, 6);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(7, 'PROD007', 'LED TV 55inch', 800.00, 999.00, 50, 10, 50, 1, 7);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(8, 'PROD008', 'Smartphone Y', 1000.00, 1399.00, 30, 35, 75, 1, 1);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(9, 'PROD009', 'Tablet Y', 350.00, 499.00, 20, 15, 50, 1, 2);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(10, 'PROD010', 'Laptop Lenav', 700.00, 899.00, 40, 20, 50, 1, 3);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(11, 'PROD011', 'Tablet cases', 30.00, 50.00, 200, 100, 300, 1, 4);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(12, 'PROD012', 'Orange Starters-pack', 8.50, 17.00, 110, 50, 150, 4, 5);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(13, 'PROD013', 'Ink cartridge', 45.00, 0.00, 0, 5, 15, 3, 6);
INSERT INTO Product (CR_Product_Product_ID, CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, CR_Product_Supplier_ID, CR_Product_Category_ID) VALUES(14, 'PROD014', 'LED TV 32inch', 300.00, 499.00, 35, 25, 50, 1, 7);

-- Dummy data for User table
INSERT INTO User (CR_User_User_ID, CR_User_UserName, CR_User_Password, CR_User_Function, CR_User_Full_Name) VALUES(1, 'asetinn66', 'password1', 'Admin', 'Mehmet Haleplioglu');
INSERT INTO User (CR_User_User_ID, CR_User_UserName, CR_User_Password, CR_User_Function, CR_User_Full_Name) VALUES(2, 'keizerkarel', 'password2', 'Cashier', 'Karel Keizer');
INSERT INTO User (CR_User_User_ID, CR_User_UserName, CR_User_Password, CR_User_Function, CR_User_Full_Name) VALUES(3, 'lizegoos', 'password3', 'Cashier', 'Lize Goos');
INSERT INTO User (CR_User_User_ID, CR_User_UserName, CR_User_Password, CR_User_Function, CR_User_Full_Name) VALUES(4, 'emmamilou', 'password4', 'Shop Assistant', 'Emma Milou');
INSERT INTO User (CR_User_User_ID, CR_User_UserName, CR_User_Password, CR_User_Function, CR_User_Full_Name) VALUES(5, 'harryhoog', 'password5', 'Technician', 'Harry Hoog');

-- Dummy data for Customer table
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(1, 'John Doe', 'john.doe@example.com', 'Belgium', '123 Main St', '1000', 'BRUSSEL', '123-456-7890', 'BE123456789');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(2, 'Jane Smith', 'jane.smith@example.com', 'Belgium', '456 Oak Ave', '2000', 'ANTWERPEN', '987-654-3210', 'BE987654321');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(3, 'Bob Johnson', 'bob.johnson@example.com', 'Belgium', '789 Pine Rd', '3500', 'HASSELT', '555-123-4567', 'BE555123456');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(4, 'Alice Brown', 'alice.brown@example.com', 'Belgium', '321 Elm St', '3600', 'GENK', '111-222-3333', 'BE111222333');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(5, 'Charlie Davis', 'charlie.davis@example.com', 'Belgium', '987 Birch Ln', '3630', 'MAASMECHELEN', '444-555-6666', 'BE444555666');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(6, 'Eva White', 'eva.white@example.com', 'Belgium', '567 Maple Dr', '3600', 'GENK', '777-888-9999', 'BE777888999');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(7, 'Frank Green', 'frank.green@example.com', 'Belgium', '234 Pine Rd', '3530', 'HOUTHALEN-HELCHTEREN', '222-333-4444', 'BE222333444');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(8, 'Grace Miller', 'grace.miller@example.com', 'Belgium', '876 Oak Ave', '1000', 'BRUSSEL', '999-888-7777', 'BE999888777');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(9, 'Harry Wilson', 'harry.wilson@example.com', 'Belgium', '765 Cedar St', '3600', 'GENK', '666-555-4444', 'BE666555444');
INSERT INTO Customer (CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, CR_Customer_VAT) VALUES(10, 'Ivy Turner', 'ivy.turner@example.com', 'Belgium', '543 Birch Ln', '3500', 'HASSELT', '333-222-1111', 'BE333222111');

-- Dummy data for Inventory table
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(1, 1, 55);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(2, 2, 30);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(3, 3, 30);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(4, 4, 400);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(5, 5, 150);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(6, 6, 10);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(7, 7, 50);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(8, 8, 30);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(9, 9, 20);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(10, 10, 40);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(11, 11, 200);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(12, 12, 110);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(13, 13, 0);
INSERT INTO Inventory (CR_Inventory_Inventory_ID, CR_Inventory_Product_ID, CR_Inventory_Stock_quantity) VALUES(14, 14, 35);

-- Dummy data for Sales Backorder table
INSERT INTO Sales_Backorder (CR_SaBackorder_Backorder_ID, CR_SaBackorder_Product_ID, CR_SaBackorder_Customer_ID, CR_SaBackorder_Date, CR_SaBackorder_Quantity, CR_SaBackorder_Status) VALUES(1, 13, 1, '2024-03-07', 15, 'In Progress');

-- Dummy data for Storage Backorder table
INSERT INTO Storage_Backorder (CR_StBackorder_Backorder_ID, CR_StBackorder_Product_ID, CR_StBackorder_Supplier_ID, CR_StBackorder_Date, CR_StBackorder_Order_Quantity, CR_StBackorder_Status) VALUES(1, 8, 1, '2024-03-07', 45, 'In Progress');

-- Dummy data for Invoice table
INSERT INTO Invoice (CR_Invoice_Invoice_ID, CR_Invoice_Customer_ID, CR_Invoice_User_ID, CR_Invoice_Date) VALUES(1, 1, 2, '2024-03-01');
INSERT INTO Invoice (CR_Invoice_Invoice_ID, CR_Invoice_Customer_ID, CR_Invoice_User_ID, CR_Invoice_Date) VALUES(2, 2, 2, '2024-03-01');
INSERT INTO Invoice (CR_Invoice_Invoice_ID, CR_Invoice_Customer_ID, CR_Invoice_User_ID, CR_Invoice_Date) VALUES(3, 1, 3, '2024-03-02');


-- Dummy data for Invoice_Line table
INSERT INTO Invoice_Line (CR_Invoice_Line_Invoice_Line_ID, CR_Invoice_Line_Invoice_ID, CR_Invoice_Line_Product_ID, CR_Invoice_Line_Order_Line_Quantity) VALUES(1, 1, 1, 2);
INSERT INTO Invoice_Line (CR_Invoice_Line_Invoice_Line_ID, CR_Invoice_Line_Invoice_ID, CR_Invoice_Line_Product_ID, CR_Invoice_Line_Order_Line_Quantity) VALUES(2, 1, 3, 1);
INSERT INTO Invoice_Line (CR_Invoice_Line_Invoice_Line_ID, CR_Invoice_Line_Invoice_ID, CR_Invoice_Line_Product_ID, CR_Invoice_Line_Order_Line_Quantity) VALUES(3, 2, 7, 1);
INSERT INTO Invoice_Line (CR_Invoice_Line_Invoice_Line_ID, CR_Invoice_Line_Invoice_ID, CR_Invoice_Line_Product_ID, CR_Invoice_Line_Order_Line_Quantity) VALUES(4, 3, 5, 3);
