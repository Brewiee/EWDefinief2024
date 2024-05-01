CREATE TABLE IF NOT EXISTS PostalCode (
    CR_PostalCode_Zipcode INT PRIMARY KEY,
    CR_PostalCode_City VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Category (
    CR_Category_Category_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Category_Name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Supplier (
    CR_Supplier_Supplier_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Supplier_Name VARCHAR(255),
    CR_Supplier_Country VARCHAR(255),
    CR_Supplier_Address VARCHAR(255),
    CR_Supplier_Zipcode INT,
    CR_Supplier_City VARCHAR(255),
    CR_Supplier_Phone_number VARCHAR(20),
    CR_Supplier_Email VARCHAR(255),
    CR_Supplier_VAT VARCHAR(255),
    FOREIGN KEY (CR_Supplier_Zipcode) REFERENCES PostalCode(CR_PostalCode_Zipcode)
);

CREATE TABLE IF NOT EXISTS Product (
    CR_Product_Product_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Product_ProductCode VARCHAR(255),
    CR_Product_Name VARCHAR(255),
    CR_Product_Price_B DECIMAL(10, 2),
    CR_Product_Price_S DECIMAL(10, 2),
    CR_Product_Stock_quantity INT,
    CR_Product_Min_Stock INT,
    CR_Product_Max_Stock INT,
    CR_Product_Supplier_ID INT,
    CR_Product_Category_ID INT,
    FOREIGN KEY (CR_Product_Category_ID) REFERENCES Category(CR_Category_Category_ID),
    FOREIGN KEY (CR_Product_Supplier_ID) REFERENCES Supplier(CR_Supplier_Supplier_ID)
);

CREATE TABLE IF NOT EXISTS User (
    CR_User_User_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_User_UserName VARCHAR(255),
    CR_User_Password VARCHAR(255),
    CR_User_Function VARCHAR(255),
    CR_User_Full_Name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Customer (
    CR_Customer_Customer_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Customer_Name VARCHAR(255),
    CR_Customer_Email VARCHAR(255),
    CR_Customer_Country VARCHAR(255),
    CR_Customer_Address VARCHAR(255),
    CR_Customer_Zipcode INT,
    CR_Customer_City VARCHAR(255),
    CR_Customer_Phone_number VARCHAR(20),
    CR_Customer_VAT VARCHAR(255),
    FOREIGN KEY (CR_Customer_Zipcode) REFERENCES PostalCode(CR_PostalCode_Zipcode)
);

CREATE TABLE IF NOT EXISTS Inventory (
    CR_Inventory_Inventory_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Inventory_Product_ID INT,
    CR_Inventory_Stock_quantity INT,
    FOREIGN KEY (CR_Inventory_Product_ID) REFERENCES Product(CR_Product_Product_ID)
);

CREATE TABLE IF NOT EXISTS Sales_Backorder (
    CR_SaBackorder_Backorder_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_SaBackorder_Product_ID INT,
    CR_SaBackorder_Customer_ID INT,
    CR_SaBackorder_Date DATE,
    CR_SaBackorder_Quantity INT,
    CR_SaBackorder_Status VARCHAR(255),
    FOREIGN KEY (CR_SaBackorder_Product_ID) REFERENCES Product(CR_Product_Product_ID),
    FOREIGN KEY (CR_SaBackorder_Customer_ID) REFERENCES Customer(CR_Customer_Customer_ID)
);

CREATE TABLE IF NOT EXISTS Storage_Backorder (
    CR_StBackorder_Backorder_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_StBackorder_Product_ID INT,
    CR_StBackorder_Supplier_ID INT,
    CR_StBackorder_Date DATE,
    CR_StBackorder_Order_Quantity INT,
    CR_StBackorder_Status VARCHAR(255),
    FOREIGN KEY (CR_StBackorder_Product_ID) REFERENCES Product(CR_Product_Product_ID),
    FOREIGN KEY (CR_StBackorder_Supplier_ID) REFERENCES Supplier(CR_Supplier_Supplier_ID)
);

CREATE TABLE IF NOT EXISTS Invoice (
    CR_Invoice_Invoice_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Invoice_Customer_ID INT,
    CR_Invoice_User_ID INT,
    CR_Invoice_Date DATE,
    FOREIGN KEY (CR_Invoice_Customer_ID) REFERENCES Customer(CR_Customer_Customer_ID),
    FOREIGN KEY (CR_Invoice_User_ID) REFERENCES User(CR_User_User_ID)
);

CREATE TABLE IF NOT EXISTS Invoice_Line (
    CR_Invoice_Line_Invoice_Line_ID INT AUTO_INCREMENT PRIMARY KEY,
    CR_Invoice_Line_Invoice_ID INT,
    CR_Invoice_Line_Product_ID INT,
    CR_Invoice_Line_Order_Line_Quantity INT,
    FOREIGN KEY (CR_Invoice_Line_Invoice_ID) REFERENCES Invoice(CR_Invoice_Invoice_ID),
    FOREIGN KEY (CR_Invoice_Line_Product_ID) REFERENCES Product(CR_Product_Product_ID)
);
