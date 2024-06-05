import textwrap
import pymysql
import datetime
import os
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QLineEdit, QMessageBox, QCompleter, QCheckBox, QDialog, QPlainTextEdit
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtCore import Qt, QDate, QStringListModel
from pymysql.cursors import DictCursor
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from CreatePostalcode import AddPostalCodeDialog

# Variables
ICON_FOLDER = "../Icons/"
windows_base_dir = "C:/Users/M.Akif Haleplioglu/PycharmProjects/Eindwerk_voorbereiding"
fedora_base_dir = ""
dbuser = "dbadmin"
dbpass = "dbadmin"
database_db = "CashRegister"

class InvoiceManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Invoice Interface")
        self.setGeometry(100, 100, 1920, 1080)

        # Initialize database connection
        self.conn = pymysql.connect(
            host="localhost",
            user=dbuser,
            password=dbpass,
            database=database_db,
            cursorclass=pymysql.cursors.DictCursor
        )

        self.init_ui()
        self.update_customer_completer()
        self.update_product_completer()

        # Hide new customer fields initially
        self.new_customer_fields_widget.setVisible(False)

        # Dictionary to temporarily store additional details
        self.additional_details_dict = {}

        # Dictionary to track temporary stock quantities
        self.temporary_stock = {}

    def init_ui(self):
        # Initialize layout
        self.layout = QVBoxLayout()

        # Base directory where the icons folder is located
        base_dir = windows_base_dir  # Change this to match your base directory on Windows

        # If running on Unix-like system, adjust the base directory
        if os.name == "posix":
            base_dir = fedora_base_dir  # Replace this with the actual path on Unix-like systems

        # Define paths to the icons
        customer_icon_path = os.path.join(base_dir, "icons", "customer.png")
        product_icon_path = os.path.join(base_dir, "icons", "product.png")
        quantity_icon_path = os.path.join(base_dir, "icons", "quantity.png")
        vat_icon_path = os.path.join(base_dir, "icons", "vat.png")

        # Existing customer fields with icon
        self.customer_label = QLabel()
        self.customer_label.setPixmap(QPixmap(customer_icon_path).scaledToWidth(20, Qt.SmoothTransformation))
        customer_text_label = QLabel("Customer:")
        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("Search customer...")
        self.customer_input.setStyleSheet("color: white;")  # Set font color to white
        self.customer_input.setFixedWidth(1400)  # Set fixed width for input field

        customer_layout = QHBoxLayout()
        customer_layout.addWidget(self.customer_label)
        customer_layout.addWidget(customer_text_label)
        customer_layout.addWidget(self.customer_input)
        self.layout.addLayout(customer_layout)

        # Add checkbox to toggle new customer fields
        self.new_customer_checkbox = QCheckBox("New Customer")
        self.new_customer_checkbox.stateChanged.connect(self.toggle_customer_fields)
        self.layout.addWidget(self.new_customer_checkbox)

        # Add new customer fields layout
        self.new_customer_fields_widget = QWidget()
        self.new_customer_fields = QVBoxLayout(self.new_customer_fields_widget)

        # Modify the icon filenames to use platform-independent paths
        icon_filenames = [
            os.path.join(ICON_FOLDER, "name.png"),
            os.path.join(ICON_FOLDER, "email.png"),
            os.path.join(ICON_FOLDER, "country.png"),
            os.path.join(ICON_FOLDER, "address.png"),
            os.path.join(ICON_FOLDER, "postal_code.png"),
            os.path.join(ICON_FOLDER, "city.png"),
            os.path.join(ICON_FOLDER, "phone.png"),
            os.path.join(ICON_FOLDER, "vat.png")
        ]

        field_labels = [
            "Name:",
            "Email:",
            "Country:",
            "Address:",
            "Postal Code:",
            "City:",
            "Phone Number:",
            "VAT:"
        ]

        self.line_edit_fields = {}  # Dictionary to store line edit fields

        # Modify the layout of new customer fields to set fixed width for labels and dynamic width for input fields
        for icon_filename, field_label in zip(icon_filenames, field_labels):
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_filename).scaledToWidth(20, Qt.SmoothTransformation))
            field_label_widget = QLabel(field_label)
            field_label_widget.setAlignment(Qt.AlignLeft)  # Align label to the left
            field_label_widget.setFixedWidth(100)  # Set fixed width for labels

            field_input = QLineEdit()
            field_input.setObjectName(field_label.replace(":", "").replace(" ", "") + "LineEdit")  # Set object name

            # Calculate the width of input field relative to the available width
            field_input.setMinimumWidth(1000)  # Set minimum width for input fields

            # Connect signal to the postal code field
            if field_label == "Postal Code:":
                field_input.editingFinished.connect(self.check_postal_code)

            layout_row = QHBoxLayout()
            layout_row.addWidget(icon_label)
            layout_row.addWidget(field_label_widget)
            layout_row.addWidget(field_input)
            layout_row.addStretch(1)  # Add stretch to push input field to the right
            self.new_customer_fields.addLayout(layout_row)
            self.line_edit_fields[field_label] = field_input  # Add line edit field to dictionary

        self.layout.addWidget(self.new_customer_fields_widget)

        self.btn_save = QPushButton("Save New Customer")
        self.btn_save.clicked.connect(self.save_new_customer)  # Connect to save_new_customer method
        self.btn_save.hide()  # Initially hide the save button
        self.layout.addWidget(self.btn_save)

        # Existing customer fields with icon
        self.product_label = QLabel()
        self.product_label.setPixmap(QPixmap(product_icon_path).scaledToWidth(20, Qt.SmoothTransformation))
        product_text_label = QLabel("Product:")
        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Search product...")
        self.product_input.setStyleSheet("color: white;")  # Set font color to white
        self.product_input.setFixedWidth(1400)  # Set fixed width for input field

        product_layout = QHBoxLayout()
        product_layout.addWidget(self.product_label)
        product_layout.addWidget(product_text_label)
        product_layout.addWidget(self.product_input)
        self.layout.addLayout(product_layout)

        # Add quantity input field with icon
        self.quantity_label = QLabel()
        self.quantity_label.setPixmap(QPixmap(quantity_icon_path).scaledToWidth(20, Qt.SmoothTransformation))
        quantity_text_label = QLabel("Quantity:")
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Input quantity...")
        self.quantity_input.setStyleSheet("color: white;")  # Set font color to white
        self.quantity_input.setFixedWidth(1400)  # Set fixed width for input field

        quantity_layout = QHBoxLayout()
        quantity_layout.addWidget(self.quantity_label)
        quantity_layout.addWidget(quantity_text_label)
        quantity_layout.addWidget(self.quantity_input)
        self.layout.addLayout(quantity_layout)

        # Add VAT input field
        self.vat_label = QLabel()
        self.vat_label.setPixmap(QPixmap(vat_icon_path).scaledToWidth(20, Qt.SmoothTransformation))
        vat_text_label = QLabel("VAT %:")
        self.vat_input = QLineEdit("21")
        self.vat_input.setFixedWidth(1400)  # Set fixed width for input field

        vat_layout = QHBoxLayout()
        vat_layout.addWidget(self.vat_label)
        vat_layout.addWidget(vat_text_label)
        vat_layout.addWidget(self.vat_input)
        self.layout.addLayout(vat_layout)

        # Add button to add product to invoice
        self.add_button = QPushButton("Add Product to Invoice")
        self.add_button.clicked.connect(self.add_product_to_invoice)
        self.layout.addWidget(self.add_button)

        # Add table view for displaying invoice details
        self.table = QTableWidget()
        # Invoice_Line columns: Product, Quantity, Unit Price, VAT_Percentage, VAT, Line Total, Product Information
        self.table.setColumnCount(11)
        # Set the width of the "Product" column
        product_column_width = self.table.columnWidth(0)
        self.table.setColumnWidth(0, product_column_width + 210)
        # Set the width of the "Product Information" column
        product_info_column_width = self.table.columnWidth(5)
        self.table.setColumnWidth(7, product_info_column_width + 170)
        self.table.setHorizontalHeaderLabels(["Product", "Quantity", "Unit Price (VAT ex)", "VAT %", "VAT",
                                              "Unit Price (VAT in)", "Line Total", "Product Information (e.g. s/n)",
                                              "", "", ""])
        self.layout.addWidget(self.table)

        # Add labels to display total VAT amounts on one line
        total_vat_layout = QHBoxLayout()
        self.total_vat_label = QLabel("Total VAT:")
        self.total_vat_amount_label = QLabel()
        total_vat_layout.addWidget(self.total_vat_label)
        total_vat_layout.addWidget(self.total_vat_amount_label)
        self.layout.addLayout(total_vat_layout)

        # Add labels to display total amounts next to each other
        total_layout = QHBoxLayout()
        self.total_label = QLabel("Total Amount:")
        self.total_amount_label = QLabel()
        total_layout.addWidget(self.total_label)
        total_layout.addWidget(self.total_amount_label)
        self.layout.addLayout(total_layout)

        # Add button to finalize and save invoice
        self.save_button = QPushButton("Save Invoice - Print Invoice to PDF")
        self.save_button.clicked.connect(self.save_invoice)
        self.layout.addWidget(self.save_button)

        # Set layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def update_customer_completer(self):
        try:
            with self.conn.cursor() as cursor:
                query = """
                    SELECT CR_Customer_Customer_ID, CR_Customer_Name, CR_Customer_Address, CR_Customer_Zipcode, 
                        CR_Customer_City, CR_Customer_VAT
                    FROM Customer
                """
                cursor.execute(query)
                customers = cursor.fetchall()
                customer_info_list = [
                    (f"{customer['CR_Customer_Customer_ID']} - {customer['CR_Customer_Name']} - "
                     f"{customer['CR_Customer_Address']} - {customer['CR_Customer_Zipcode']} - "
                     f"{customer['CR_Customer_City']} - {customer['CR_Customer_VAT']}")
                    for customer in customers
                ]
                completer = QCompleter()
                model = QStringListModel()
                model.setStringList(customer_info_list)
                completer.setModel(model)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)  # Enable searching within the fields
                self.customer_input.setCompleter(completer)
        except pymysql.Error as e:
            QMessageBox.warning(self, "Error", f"Error accessing database: {str(e)}")

    def toggle_customer_fields(self):
        # Store the current window state
        current_state = self.windowState()

        if self.new_customer_checkbox.isChecked():
            self.new_customer_fields_widget.setVisible(True)
            self.btn_save.show()  # Show the save button
        else:
            self.new_customer_fields_widget.setVisible(False)
            self.btn_save.hide()  # Hide the save button

        # Restore the window state
        self.setWindowState(current_state)

    def check_postal_code(self):
        postal_code_text = self.line_edit_fields["Postal Code:"].text()
        try:
            postal_code = int(postal_code_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Postal Code must be a valid integer.")
            return

        # Check if the entered postal code exists in the postalcode table
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT * FROM postalcode WHERE CR_PostalCode_Zipcode = %s", (postal_code,))
            existing_postal_code = cursor.fetchone()

        if existing_postal_code:
            city_line_edit = self.line_edit_fields["City:"]
            city_line_edit.setText(existing_postal_code["CR_PostalCode_City"])
            city_line_edit.setReadOnly(True)  # Make the city field read-only

        else:
            # If postal code doesn't exist, prompt user to add it
            reply = QMessageBox.question(self, "Postal Code Not Found",
                                         "Entered Postal Code does not exist. Do you want to add it?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                dialog = AddPostalCodeDialog(postal_code_text)  # No need to pass any arguments
                dialog.conn = self.conn  # Assign the database connection
                dialog.postal_code_saved.connect(self.handle_new_postal_code)  # Connect to signal
                dialog.exec()

    def handle_new_postal_code(self, postal_code, city):
        # Update the city field in the main application
        city_line_edit = self.line_edit_fields["City:"]
        city_line_edit.setText(city)
        city_line_edit.setReadOnly(True)  # Make the city field read-only

        # Update the corresponding row in the table
        for row in range(self.table.rowCount()):
            postal_code_item = self.table.item(row, 5)
            if postal_code_item and postal_code_item.text() == postal_code:
                city_item = QTableWidgetItem(city)
                city_item.setFlags(city_item.flags() & ~Qt.ItemIsEditable)  # Make city field read-only
                self.table.setItem(row, 6, city_item)

    def save_new_customer(self):
        try:
            # Get customer details from the input fields
            name = self.get_line_edit_text("Name:")
            email = self.get_line_edit_text("Email:")
            country = self.get_line_edit_text("Country:")
            address = self.get_line_edit_text("Address:")
            postal_code_text = self.get_line_edit_text("Postal Code:")
            city = self.get_line_edit_text("City:")
            phone = self.get_line_edit_text("Phone Number:")
            vat = self.get_line_edit_text("VAT:")

            try:
                postal_code = int(postal_code_text)
            except ValueError:
                QMessageBox.warning(self, "Error", "Postal Code must be a valid integer.")
                return

            # Check if all fields are filled
            if not name or not email or not country or not address or not postal_code or not city or not phone:
               QMessageBox.warning(self, "Warning", "Please fill in all fields, VAT is not required.")
               return

            # Save the new customer to the database
            with self.conn.cursor() as cursor:
                query = ("INSERT INTO Customer (CR_Customer_Name, CR_Customer_Email, CR_Customer_Country, "
                         "CR_Customer_Address, CR_Customer_Zipcode, CR_Customer_City, CR_Customer_Phone_number, "
                         "CR_Customer_VAT) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(query, (name, email, country, address, postal_code, city, phone, vat))
                self.conn.commit()

            # Clear input fields after successful save
            for widget in self.new_customer_fields_widget.findChildren(QLineEdit):
                widget.clear()
            QMessageBox.information(self, "Success", "New customer added successfully.")
            # Hide new customer fields initially
            self.new_customer_fields_widget.setVisible(False)
            self.new_customer_checkbox.setChecked(False)
            self.update_customer_completer()
        except pymysql.Error as e:
            QMessageBox.warning(self, "Error", f"Error saving new customer: {str(e)}")

    def get_line_edit_text(self, label_text):
        for i in range(self.new_customer_fields.count()):
            layout = self.new_customer_fields.itemAt(i)
            if layout is not None and isinstance(layout, QHBoxLayout):
                label = layout.itemAt(1).widget()  # Assuming label is at index 1
                if label.text() == label_text:
                    line_edit = layout.itemAt(2).widget()  # Assuming QLineEdit is at index 2
                    return line_edit.text()
        return ""

    def update_product_completer(self, sold_product_id=None, sold_quantity=0):
        try:
            with self.conn.cursor() as cursor:
                query = """
                    SELECT P.CR_Product_Product_ID, P.CR_Product_ProductCode, P.CR_Product_Name, 
                           P.CR_Product_Price_S, P.CR_Product_Stock_quantity, S.CR_Supplier_Name, 
                           C.CR_Category_Name, P.CR_Product_DateIn
                    FROM Product P
                    JOIN Supplier S ON P.CR_Product_Supplier_ID = S.CR_Supplier_Supplier_ID
                    JOIN Category C ON P.CR_Product_Category_ID = C.CR_Category_Category_ID
                """
                cursor.execute(query)
                products = cursor.fetchall()

                # Adjust the stock quantities based on sold product
                if sold_product_id and sold_quantity:
                    for product in products:
                        if product['CR_Product_Product_ID'] == sold_product_id:
                            product['CR_Product_Stock_quantity'] -= sold_quantity

                product_info_list = [
                    f"{product['CR_Product_Product_ID']} - {product['CR_Product_ProductCode']} - "
                    f"{product['CR_Product_Name']} - {product['CR_Product_Price_S']} - "
                    f"{product['CR_Product_Stock_quantity']} - {product['CR_Supplier_Name']} - "
                    f"{product['CR_Category_Name']} - {product['CR_Product_DateIn']}"
                    for product in products
                ]
                completer = QCompleter()
                model = QStringListModel()
                model.setStringList(product_info_list)
                completer.setModel(model)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)  # Enable searching within the fields
                self.product_input.setCompleter(completer)
        except pymysql.Error as e:
            QMessageBox.warning(self, "Error", f"Error accessing database: {str(e)}")

    def add_product_to_invoice(self):
        try:
            # Get customer details from customer_input
            customer_details = self.customer_input.text().split(" - ")
            if len(customer_details) < 6:
                QMessageBox.warning(self, "Error", "Invalid customer details format.")
                return

            customer_id = int(customer_details[0])  # Ensure customer_id is an integer
            customer_name = customer_details[1]
            customer_address = customer_details[2]
            customer_zipcode = customer_details[3]
            customer_city = customer_details[4]
            customer_vat = customer_details[5]

            # Get selected product details from product_input
            product_details = self.product_input.text().split(" - ")
            if len(product_details) < 5:
                raise ValueError("Invalid product details format.")

            product_id = int(product_details[0])
            product_name = product_details[2]
            unit_price = float(product_details[3])
            quantity = int(self.quantity_input.text())
            vat_percentage = float(self.vat_input.text())

            # Check stock availability
            current_stock = self.get_product_stock(product_id)
            if quantity > current_stock:
                result = QMessageBox.question(
                    self,
                    "Stock Warning",
                    f"Not enough stock for {product_name}. Available quantity: {current_stock}.\n"
                    "Would you like to proceed with a backorder?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if result == QMessageBox.No:
                    return
                else:
                    backorder_quantity = quantity - current_stock
                    self.handle_backorder(product_id, customer_id, backorder_quantity)

            # Calculate VAT value from the unit price
            vat_value = unit_price * vat_percentage / (100 + vat_percentage)
            unit_price_ex_vat = unit_price - vat_value
            line_total = quantity * unit_price

            # Add product details to the invoice table
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            self.table.setItem(row_position, 0, self.create_read_only_item(product_name))
            self.table.setItem(row_position, 1, self.create_read_only_item(str(quantity)))
            self.table.setItem(row_position, 2, self.create_read_only_item(f"{unit_price_ex_vat:.2f}"))
            self.table.setItem(row_position, 3, self.create_read_only_item(f"{vat_percentage}"))
            self.table.setItem(row_position, 4, self.create_read_only_item(f"{vat_value:.2f}"))
            self.table.setItem(row_position, 5, self.create_read_only_item(f"{unit_price:.2f}"))
            self.table.setItem(row_position, 6, self.create_read_only_item(f"{line_total:.2f}"))
            self.table.setItem(row_position, 7, self.create_read_only_item(""))

            # Add a button for adding additional details
            add_details_button = QPushButton("Add Detail")
            add_details_button.clicked.connect(lambda: self.open_additional_details_dialog(row_position))
            self.table.setCellWidget(row_position, 8, add_details_button)

            # Add a button for deleting the row
            delete_button = QPushButton("Delete", self)
            delete_button.clicked.connect(self.delete_product)
            # Store row position as custom property
            delete_button.setProperty("row_position", row_position)
            # Store column position as custom property
            delete_button.setProperty("col_position", 9)
            # Assuming the delete button is placed in column 9
            self.table.setCellWidget(row_position, 9, delete_button)

            # Add a button for updating the unit price
            update_button = QPushButton("Update Price", self)
            update_button.clicked.connect(lambda: self.open_update_price_dialog(row_position))
            self.table.setCellWidget(row_position, 10, update_button)

            # Initialize additional details list
            self.additional_details_dict[row_position] = []

            # Clear product_input, quantity_input, and vat_input fields
            self.product_input.clear()
            self.quantity_input.clear()
            self.vat_input.setText("21")

            # Track the quantity and update stock temporarily
            self.update_stock_temporary(product_id, quantity)

            # Calculate and update total amount
            self.calculate_total()

        except (ValueError, pymysql.Error) as e:
            QMessageBox.warning(self, "Error", f"Error adding product to invoice: {str(e)}")

    def update_stock_temporary(self, product_id, quantity):
        self.update_product_completer(product_id, quantity)

    def get_product_stock(self, product_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT CR_Product_Stock_quantity FROM Product WHERE CR_Product_Product_ID = %s", (product_id,))
                result = cursor.fetchone()
                if result:
                    return result['CR_Product_Stock_quantity']
                else:
                    raise ValueError("Product not found in the database.")
        except pymysql.Error as db_error:
            QMessageBox.warning(self, "Database Error", f"Database error: {str(db_error)}")
            raise

    def handle_backorder(self, product_id, customer_id, backorder_quantity):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO Sales_Backorder (CR_SaBackorder_Product_ID, CR_SaBackorder_Customer_ID, 
                                                 CR_SaBackorder_Date, CR_SaBackorder_Quantity, CR_SaBackorder_Status)
                    VALUES (%s, %s, CURDATE(), %s, 'Pending')
                    """,
                    (product_id, customer_id, backorder_quantity)
                )
                self.conn.commit()
                QMessageBox.information(self, "Backorder",
                                        f"A backorder for {backorder_quantity} units of the product has been created.")
        except pymysql.Error as db_error:
            QMessageBox.warning(self, "Database Error", f"Error creating backorder: {str(db_error)}")
            self.db.rollback()

    def get_customer_id(self):
        try:
            customer_details = self.customer_input.text().split(" - ")
            if len(customer_details) < 6:
                raise ValueError("Invalid customer details format.")
            customer_id = int(customer_details[0])
            return customer_id
        except ValueError:
            raise ValueError("Invalid customer ID. Please enter a valid integer.")

    def open_additional_details_dialog(self, row_position):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Additional Details")
        layout = QVBoxLayout()

        details_input = QPlainTextEdit()
        layout.addWidget(details_input)

        save_button = QPushButton("Save Details", dialog)
        save_button.clicked.connect(lambda: self.save_additional_details(row_position,
                                                                         details_input.toPlainText(), dialog))
        layout.addWidget(save_button)

        dialog.setLayout(layout)
        dialog.exec()

    def save_additional_details(self, row_position, details, dialog):
        if details:
            if row_position not in self.additional_details_dict:
                self.additional_details_dict[row_position] = []
            self.additional_details_dict[row_position].append(details)
            self.table.setItem(row_position, 7,
                               self.create_read_only_item("\n".join(self.additional_details_dict[row_position])))
        dialog.accept()

    def open_update_price_dialog(self, row_position):
        dialog = QDialog(self)
        dialog.setWindowTitle("Update Unit Price")
        layout = QVBoxLayout()

        price_input = QLineEdit()
        price_input.setPlaceholderText("Enter new unit price")
        layout.addWidget(price_input)

        update_button = QPushButton("Update", dialog)
        update_button.clicked.connect(lambda: self.update_unit_price(row_position, price_input.text(), dialog))
        layout.addWidget(update_button)

        dialog.setLayout(layout)
        dialog.exec()

    def update_unit_price(self, row_position, new_price, dialog):
        try:
            new_price = float(new_price)
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid unit price format.")
            return

        quantity = int(self.table.item(row_position, 1).text())
        vat_percentage = float(self.table.item(row_position, 3).text())

        # Calculate new VAT value, unit price excluding VAT, and line total
        vat_value = new_price * vat_percentage / (100 + vat_percentage)
        unit_price_ex_vat = new_price - vat_value
        line_total = quantity * new_price

        # Update the table with new values
        self.table.setItem(row_position, 2, self.create_read_only_item(f"{unit_price_ex_vat:.2f}"))
        self.table.setItem(row_position, 4, self.create_read_only_item(f"{vat_value:.2f}"))
        self.table.setItem(row_position, 5, self.create_read_only_item(f"{new_price:.2f}"))
        self.table.setItem(row_position, 6, self.create_read_only_item(f"{line_total:.2f}"))

        # Update the total amount
        self.calculate_total()

        dialog.accept()

    def create_read_only_item(self, text):
        item = QTableWidgetItem(text)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    def delete_product(self):
        # Get the sender of the signal
        sender = self.sender()
        # Retrieve the custom property (row position)
        row_position = sender.property("row_position")
        # Retrieve the custom property (col position)
        col_position = sender.property("col_position")

        if row_position is not None and col_position is not None:
            self.table.removeRow(row_position)
            # Update the row_position property of delete buttons below the deleted row
            for row in range(row_position, self.table.rowCount()):
                # Assuming the delete button is in column 9
                button = self.table.cellWidget(row, 9)
                if button:
                    # Update the row_position property
                    button.setProperty("row_position", row)
                    # Disconnect the previous connection
                    button.clicked.disconnect()
                    # Connect to delete_product method with updated row position
                    button.clicked.connect(self.delete_product)
            # Recalculate total amount after deletion
            self.calculate_total()

    def calculate_total(self):
        total_amount = 0
        total_vat = 0
        for row in range(self.table.rowCount()):
            unit_price_ex_vat = float(self.table.item(row, 2).text())
            vat_value = float(self.table.item(row, 4).text())
            line_total = float(self.table.item(row, 6).text())
            # VAT value multiplied by the quantity
            total_vat += vat_value * int(self.table.item(row, 1).text())
            total_amount += line_total

        self.total_amount_label.setText(f"€ {total_amount:.2f}")
        self.total_vat_amount_label.setText(f"€ {total_vat:.2f}")

    def save_invoice(self):
        try:
            # Get customer ID from customer_input
            customer_details = self.customer_input.text().split(" - ")
            if len(customer_details) < 1:
                raise ValueError("Invalid customer details format.")

            try:
                customer_id = int(customer_details[0])
            except ValueError:
                raise ValueError("Invalid customer ID format.")

            # Get invoice date
            invoice_date = QDate.currentDate().toString(Qt.ISODate)

            # Save invoice header
            with self.conn.cursor() as cursor:
                cursor.execute("INSERT INTO Invoice (CR_Invoice_Customer_ID, CR_Invoice_Date) VALUES (%s, %s)",
                               (customer_id, invoice_date))
                invoice_id = cursor.lastrowid

            # Save invoice lines
            for row in range(self.table.rowCount()):
                product_id = self.table.item(row, 0).text()
                quantity_str = self.table.item(row, 1).text()
                unit_price_str = self.table.item(row, 2).text()
                vat_value_str = self.table.item(row, 3).text()
                additional_details = self.additional_details_dict.get(row, [])

                try:
                    quantity = int(quantity_str)
                    unit_price = float(unit_price_str)
                    vat_value = float(vat_value_str)
                except ValueError:
                    raise ValueError(
                        f"Invalid numeric value for quantity ({quantity_str}) or unit price ({unit_price_str}), "
                        f"or VAT value ({vat_value_str}).")

                with self.conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Invoice_Line (CR_Invoice_Line_Invoice_ID, CR_Invoice_Line_Product_ID, 
                                                 CR_Invoice_Line_Order_Line_Quantity, CR_Invoice_Line_VAT_Percentage)
                        VALUES (%s, (SELECT CR_Product_Product_ID FROM Product WHERE CR_Product_Name = %s), %s, %s)
                    """, (invoice_id, product_id, quantity, vat_value))
                    invoice_line_id = cursor.lastrowid

                    # Save additional details
                    for detail in additional_details:
                        cursor.execute("""
                            INSERT INTO Additional_Detail (CR_Additional_Detail_Invoice_Line_ID, CR_Additional_Detail_Text)
                            VALUES (%s, %s)
                        """, (invoice_line_id, detail))
            self.conn.commit()
            self.print_products_to_pdf(invoice_id)

            # Clear invoice table and total amount label
            self.table.clearContents()
            self.table.setRowCount(0)
            total_amount = 0
            total_vat = 0
            self.total_amount_label.setText(f"€ {total_amount:.2f}")
            self.total_vat_amount_label.setText(f"€ {total_vat:.2f}")
            self.customer_input.clear()
            self.additional_details_dict.clear()

        except (ValueError, pymysql.Error) as e:
            self.conn.rollback()
            QMessageBox.warning(self, "Error", f"Failed to save invoice: {str(e)}")

    def print_products_to_pdf(self, invoice_id):
        # Generate invoice number
        current_year = datetime.datetime.now().year
        invoice_number = f"{current_year}-{invoice_id:04d}"

        # Company details
        company_name = "Company Name"
        company_address = "Company Address"
        company_phone = "Company Phone"
        company_email = "Company Email"
        company_vat = "Company VAT"

        # Determine the path to save the invoice PDF
        user_home = os.path.expanduser("~")
        company_folder = os.path.join(user_home, company_name)
        invoice_folder = os.path.join(company_folder, "Invoices")
        if not os.path.exists(invoice_folder):
            os.makedirs(invoice_folder)

        pdf_file_path = os.path.join(invoice_folder, f"Invoice_{invoice_number}.pdf")

        # Create a PDF document
        c = canvas.Canvas(pdf_file_path, pagesize=letter)
        width, height = letter

        # Company information header
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(560, height - 70, company_name)
        c.setFont("Helvetica", 10)
        c.drawRightString(560, height - 85, company_address)
        c.drawRightString(560, height - 100, f"Phone: {company_phone}")
        c.drawRightString(560, height - 115, f"Email: {company_email}")
        c.setFont("Helvetica", 10)
        c.drawRightString(560, height - 130, company_vat)

        # Title
        c.setFont("Helvetica-Bold", 22)
        c.drawString(270, height - 40, "Invoice")

        # Invoice number
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, height - 70, f"Invoice Number: {invoice_number}")

        # Extract customer details
        customer_details = self.customer_input.text().split(" - ")
        if len(customer_details) < 6:
            QMessageBox.warning(self, "Error", "Invalid customer details format.")
            return

        customer_id = customer_details[0]
        customer_name = customer_details[1]
        customer_address = customer_details[2]
        customer_zipcode = customer_details[3]
        customer_city = customer_details[4]
        customer_vat = customer_details[5]

        # Customer information
        c.setFont("Helvetica", 10)
        y = height - 100
        c.drawString(40, y, f"Customer ID: {customer_id}")
        y -= 15
        c.drawString(40, y, f"Name: {customer_name}")
        y -= 15
        c.drawString(40, y, f"Address: {customer_address}")
        y -= 15
        c.drawString(40, y, f"Zipcode: {customer_zipcode}")
        y -= 15
        c.drawString(40, y, f"City: {customer_city}")
        y -= 15
        c.drawString(40, y, f"VAT: {customer_vat}")
        y -= 15
        c.drawString(40, y, f"Date: {QDate.currentDate().toString(Qt.ISODate)}")
        y -= 50

        # Table header
        c.setFont("Helvetica-Bold", 10)
        c.drawString(40, y, "Product")
        c.drawString(230, y, "Quantity")
        c.drawString(300, y, "Unit Price (VAT ex.)")
        c.drawString(410, y, "VAT")
        c.drawString(470, y, "Line Total (VAT in.)")
        y -= 20

        # Table content
        c.setFont("Helvetica", 10)
        for row in range(self.table.rowCount()):
            product_name = self.table.item(row, 0).text()
            quantity = self.table.item(row, 1).text()
            unit_price = self.table.item(row, 2).text()
            vat_value = self.table.item(row, 4).text()
            line_total = self.table.item(row, 6).text()
            additional_details = self.additional_details_dict.get(row, "")

            # Calculate the space needed for product name
            product_name_width = c.stringWidth(product_name)

            # Determine if product name needs to be split into multiple lines
            if product_name_width > 190:  # Adjust based on available space
                # Split product name into lines that fit
                lines = textwrap.wrap(product_name, width=38)  # Adjust width as needed
                for index, line in enumerate(lines):
                    c.drawString(40, y, line)
                    if index == len(lines) - 1:
                        # If it's the last line of the product name, align the quantity
                        c.drawString(230, y, quantity)
                        c.drawString(300, y, unit_price)
                        c.drawString(410, y, vat_value)
                        c.drawString(470, y, line_total)
                    y -= 15
            else:
                c.drawString(40, y, product_name)
                c.drawString(230, y, quantity)  # Draw quantity aligned with the product name
                c.drawString(300, y, unit_price)
                c.drawString(410, y, vat_value)
                c.drawString(470, y, line_total)
                y -= 15


            if additional_details:
                details_string = "\n".join(additional_details)
                for detail in details_string.splitlines():  # Split by newline character
                    c.drawString(70, y, detail)
                    y -= 15

        # Total amounts
        y -= 50
        c.setFont("Helvetica-Bold", 10)
        c.drawString(350, y, "Total VAT :")
        c.drawRightString(480, y, self.total_vat_amount_label.text())
        y -= 15
        c.drawString(350, y, "Total Amount :")
        c.drawRightString(480, y, self.total_amount_label.text())

        # Save the PDF
        c.save()

        # Adjust product stock quantities
        self.adjust_product_stock_quantities(invoice_id)

        # Check for backorders for each product in the invoice
        self.check_backorders(invoice_id)

        reply = QMessageBox.information(self, "Success",
                                        f"Invoice saved successfully as {pdf_file_path}. Do you want to open it?",
                                        QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            # Open the PDF file after it's saved
            if os.name == 'nt':  # Check if running on Windows
                os.startfile(pdf_file_path)
            elif os.name == 'posix':  # Check if running on Unix-like system
                os.system(f"xdg-open {pdf_file_path}")

    def adjust_product_stock_quantities(self, invoice_id):
        try:
            with self.conn.cursor(DictCursor) as cursor:
                # Fetch products in the current invoice
                cursor.execute("""
                                    SELECT il.CR_Invoice_Line_Invoice_ID, il.CR_Invoice_Line_Product_ID, 
                                        il.CR_Invoice_Line_Order_Line_Quantity
                                    FROM Invoice_Line il
                                    JOIN Product p ON p.CR_Product_Product_ID = il.CR_Invoice_Line_Product_ID
                                    WHERE il.CR_Invoice_Line_Invoice_ID = %s
                                """, (invoice_id,))
                products_in_invoice = cursor.fetchall()

                # Update product stock quantities
                for product in products_in_invoice:
                    product_id = product['CR_Invoice_Line_Product_ID']
                    quantity = product['CR_Invoice_Line_Order_Line_Quantity']

                    cursor.execute("""
                        UPDATE Product p
                        JOIN Invoice_Line il ON p.CR_Product_Product_ID = il.CR_Invoice_Line_Product_ID
                        SET p.CR_Product_Stock_quantity = p.CR_Product_Stock_quantity - %s
                        WHERE il.CR_Invoice_Line_Invoice_ID = %s AND p.CR_Product_Product_ID = %s
                    """, (quantity, invoice_id, product_id))

                self.conn.commit()

        except pymysql.Error as e:
            QMessageBox.critical(self, 'Error', f"Error adjusting product stock quantities: {str(e)}")

    def check_backorders(self, invoice_id):
        try:
            with self.conn.cursor() as cursor:
                # Fetch products in the current invoice
                cursor.execute("""
                    SELECT p.CR_Product_Product_ID, p.CR_Product_Name, p.CR_Product_Stock_quantity,
                           p.CR_Product_Min_Stock, p.CR_Product_Max_Stock
                    FROM Product p
                    JOIN Invoice_Line il ON p.CR_Product_Product_ID = il.CR_Invoice_Line_Product_ID
                    WHERE il.CR_Invoice_Line_Invoice_ID = %s
                """, (invoice_id,))
                products_in_invoice = cursor.fetchall()

                # Process each product in the invoice
                for product in products_in_invoice:
                    # Check if there is already a pending backorder for this product
                    cursor.execute("""
                        SELECT COUNT(*) 
                        FROM Storage_Backorder 
                        WHERE CR_StBackorder_Product_ID = %s 
                        AND CR_StBackorder_Status = 'Pending'
                    """, (product['CR_Product_Product_ID'],))
                    pending_backorders = cursor.fetchone()['COUNT(*)']

                    # If there are no pending backorders, proceed to check the stock level
                    if pending_backorders == 0:
                        # Check if the product needs to be reordered
                        if product['CR_Product_Stock_quantity'] < product['CR_Product_Min_Stock']:
                            # Calculate reorder quantity
                            reorder_quantity = product['CR_Product_Max_Stock'] - product['CR_Product_Stock_quantity']

                            # Ask the user if they want to reorder the product
                            reply = QMessageBox.question(self, 'Reorder Product',
                                                         f"The stock quantity of {product['CR_Product_Name']} is lower than the minimum stock level. "
                                                         f"Do you want to reorder {reorder_quantity} units of this product?",
                                                         QMessageBox.Yes | QMessageBox.No)

                            # If the user confirms, save the reorder details
                            if reply == QMessageBox.Yes:
                                self.save_stbackorder(product['CR_Product_Product_ID'], reorder_quantity)

        except pymysql.Error as e:
            QMessageBox.critical(self, 'Error', f"Error checking backorders for invoice: {str(e)}")

    def save_stbackorder(self, product_id, reorder_quantity):
        try:
            # Fetch supplier details for the product
            supplier_details = self.fetch_supplier_details(product_id)

            with self.conn.cursor() as cursor:
                # Save backorder details in Storage_Backorder table
                sql = """
                    INSERT INTO Storage_Backorder (CR_StBackorder_Product_ID, CR_StBackorder_Supplier_ID, 
                        CR_StBackorder_Date, CR_StBackorder_Order_Quantity, CR_StBackorder_Status) 
                    VALUES (%s, %s, CURDATE(), %s, %s)
                """
                cursor.execute(sql, (product_id, supplier_details['CR_Supplier_Supplier_ID'],
                                     reorder_quantity, 'Pending'))
                self.conn.commit()

                QMessageBox.information(self, 'Success', 'Backorder placed successfully for this product.')

        except pymysql.Error as e:
            QMessageBox.critical(self, 'Error', f"Error saving backorder: {str(e)}")

    def fetch_supplier_details(self, product_id):
        try:
            with self.conn.cursor() as cursor:
                # Fetch supplier details for the product
                sql = """
                    SELECT s.CR_Supplier_Supplier_ID, s.CR_Supplier_Name, s.CR_Supplier_Email,
                           s.CR_Supplier_Country, s.CR_Supplier_Address, s.CR_Supplier_Zipcode,
                           s.CR_Supplier_City, s.CR_Supplier_Phone_number, s.CR_Supplier_VAT
                    FROM Supplier s
                    JOIN Product p ON s.CR_Supplier_Supplier_ID = p.CR_Product_Supplier_ID
                    WHERE p.CR_Product_Product_ID = %s
                """
                cursor.execute(sql, (product_id,))
                supplier_details = cursor.fetchone()

                return supplier_details

        except pymysql.Error as e:
            QMessageBox.critical(self, 'Error', f"Error fetching supplier details: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set Fusion style
    app.setStyle("Fusion")

    # Set dark mode palette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = InvoiceManagementApp()
    window.showMaximized()  # Open window in full-screen mode
    sys.exit(app.exec())
