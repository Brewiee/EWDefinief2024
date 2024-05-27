from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QCheckBox, QHBoxLayout, QFileDialog, QComboBox
from PySide6.QtGui import QColor, QPalette, QIcon, QPixmap, QGuiApplication
from PySide6.QtCore import Qt
import sys
import os
import decimal
from fpdf import FPDF
from datetime import datetime, date
import pymysql


# Variables
ICON_FOLDER = "../Icons/"
windows_base_dir = "C:/Users/M.Akif Haleplioglu/PycharmProjects/Eindwerk_voorbereiding"
fedora_base_dir = ""
dbuser = "dbadmin"
dbpass = "dbadmin"
database_db = "CashRegister"

class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value):
        super().__init__(str(value))

    def __lt__(self, other):
        if (isinstance(other, QTableWidgetItem)):
            try:
                return float(self.text()) < float(other.text())
            except ValueError:
                return self.text() < other.text()
        else:
            return QTableWidgetItem.__lt__(self, other)

class ProductManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Product Management")
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
        self.populate_table()

        # Hide new product fields initially
        self.new_product_fields_widget.setVisible(False)

    def init_ui(self):
        self.layout = QVBoxLayout()  # Define QVBoxLayout as instance variable

        # Add checkbox to toggle new product fields
        self.new_product_checkbox = QCheckBox("New Product")
        self.new_product_checkbox.stateChanged.connect(self.toggle_product_fields)
        self.layout.addWidget(self.new_product_checkbox)

        # Add new product fields layout
        self.new_product_fields_widget = QWidget()
        self.new_product_fields = QVBoxLayout(self.new_product_fields_widget)

        # Base directory where the icons folder is located
        base_dir = windows_base_dir  # Change this to match your base directory on Windows

        # If running on Unix-like system, adjust the base directory
        if os.name == "posix":
            base_dir = fedora_base_dir  # Replace this with the actual path on Unix-like systems

        # Modify the icon filenames to use platform-independent paths
        icon_filenames = [
            os.path.join(ICON_FOLDER, "barcode.png"),
            os.path.join(ICON_FOLDER, "name.png"),
            os.path.join(ICON_FOLDER, "purchase.png"),
            os.path.join(ICON_FOLDER, "selling.png"),
            os.path.join(ICON_FOLDER, "stock.png"),
            os.path.join(ICON_FOLDER, "min.png"),
            os.path.join(ICON_FOLDER, "max.png"),
            os.path.join(ICON_FOLDER, "supplier.png"),
            os.path.join(ICON_FOLDER, "category.png"),
        ]

        field_labels = [
            "Product code:",
            "Product name:",
            "Purchase price:",
            "Selling price:",
            "Stock quantity:",
            "Minimum stock:",
            "Maximum stock:",
            "Supplier:",
            "Category:"
        ]

        self.line_edit_fields = {}  # Dictionary to store line edit fields

        # Modify the layout of new product fields to set fixed width for labels and dynamic width for input fields
        for icon_filename, field_label in zip(icon_filenames, field_labels):
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_filename).scaledToWidth(20, Qt.SmoothTransformation))
            field_label_widget = QLabel(field_label)
            field_label_widget.setAlignment(Qt.AlignLeft)  # Align label to the left
            field_label_widget.setFixedWidth(100)  # Set fixed width for labels

            layout_row = QHBoxLayout()
            layout_row.addWidget(icon_label)
            layout_row.addWidget(field_label_widget)

            if field_label == "Supplier:":
                # Add combo box for selecting supplier
                self.supplier_combo_box = QComboBox()
                self.supplier_combo_box.addItem("")  # Add empty item
                self.populate_supplier_combo_box()
                self.supplier_combo_box.setFixedWidth(1000)  # Set custom width for the combo box
                layout_row.addWidget(self.supplier_combo_box)
            elif field_label == "Category:":
                # Add combo box for selecting category
                self.category_combo_box = QComboBox()
                self.category_combo_box.addItem("")  # Add empty item
                self.populate_category_combo_box()
                self.category_combo_box.setFixedWidth(1000)  # Set custom width for the combo box
                layout_row.addWidget(self.category_combo_box)
            else:
                field_input = QLineEdit()
                field_input.setObjectName(field_label.replace(":", "").replace(" ", "") + "LineEdit")  # Set object name

                # Calculate the width of input field relative to the available width
                field_input.setMinimumWidth(1000)  # Set minimum width for input fields

                layout_row.addWidget(field_input)
                self.new_product_fields.addLayout(layout_row)
                self.line_edit_fields[field_label] = field_input  # Add line edit field to dictionary

                #layout_row.addWidget(field_input)
                #self.line_edit_fields[field_label] = field_input  # Add line edit field to dictionary

            layout_row.addStretch(1)  # Add stretch to push input field to the right
            self.new_product_fields.addLayout(layout_row)

        self.supplier_id = None
        self.category_id = None

        self.supplier_combo_box.currentIndexChanged.connect(self.update_supplier_id)
        self.category_combo_box.currentIndexChanged.connect(self.update_category_id)

        self.layout.addWidget(self.new_product_fields_widget)

        self.btn_save = QPushButton("Save New Product")
        self.btn_save.clicked.connect(self.save_new_product)  # Connect to save_new_product method
        self.btn_save.hide()  # Initially hide the save button
        self.layout.addWidget(self.btn_save)

        # Add search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setStyleSheet("color: white;")  # Set font color to white
        self.search_input.textChanged.connect(self.filter_products)
        self.layout.addWidget(self.search_input)

        # Add table view for products
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Product Code", "Product Name", "Purchase Price", "Selling Price", "Stock Quantity", "Min. Stock",
             "Max. Stock", "Supplier", "Category", "Date In Stock"])
        self.layout.addWidget(self.table)

        # Set sorting enabled for the table
        self.table.setSortingEnabled(True)

        # Add save button
        self.btn_save_changes = QPushButton("Save Changes")
        self.btn_save_changes.clicked.connect(self.save_changes)
        self.layout.addWidget(self.btn_save_changes)

        # Print Button
        self.btn_print_pdf = QPushButton("Print Product List to PDF")
        self.btn_print_pdf.clicked.connect(self.print_products_to_pdf)
        self.layout.addWidget(self.btn_print_pdf)

        # Set layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def populate_table(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        p.CR_Product_Product_ID,
                        p.CR_Product_ProductCode,
                        p.CR_Product_Name,
                        p.CR_Product_Price_B,
                        p.CR_Product_Price_S,
                        p.CR_Product_Stock_quantity,
                        p.CR_Product_Min_Stock,
                        p.CR_Product_Max_Stock,
                        s.CR_Supplier_Name,  -- Fetch supplier_name from Supplier table
                        c.CR_Category_Name,  -- Fetch category_name from Category table
                        p.CR_Product_DateIn
                    FROM 
                        Product p
                    INNER JOIN 
                        Supplier s ON p.CR_Product_Supplier_ID = s.CR_Supplier_Supplier_ID
                    INNER JOIN 
                        Category c ON p.CR_Product_Category_ID = c.CR_Category_Category_ID
                """)
                products = cursor.fetchall()

                self.table.setRowCount(len(products))
                for row, product in enumerate(products):
                    for col, field in enumerate(product.values()):
                        if col in [0, 1, 2, 3, 8, 9, 10]:  # Read-only columns
                            if col in [0, 3]:  # Numeric fields
                                item = NumericTableWidgetItem(str(field))
                            else:  # Default for other fields
                                item = QTableWidgetItem(str(field))
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                        elif col in [4, 5, 6, 7]:  # Numeric fields
                            item = NumericTableWidgetItem(str(field))
                        else:  # Default for other fields
                            item = QTableWidgetItem(str(field))

                        self.table.setItem(row, col, item)

                # Resize columns to fit content
                self.table.resizeColumnsToContents()

            # Sort the table by ID after populating
            self.table.sortByColumn(0, Qt.AscendingOrder)

        except pymysql.Error as e:
            print("Error:", e)

    def populate_supplier_combo_box(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT CR_Supplier_Supplier_ID, CR_Supplier_Name FROM Supplier")
                suppliers = cursor.fetchall()
                for supplier in suppliers:
                    self.supplier_combo_box.addItem(supplier["CR_Supplier_Name"], supplier["CR_Supplier_Supplier_ID"])
        except pymysql.Error as e:
            print("Error:", e)

    def populate_category_combo_box(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT CR_Category_Category_ID, CR_Category_Name FROM Category")
                categories = cursor.fetchall()
                for category in categories:
                    self.category_combo_box.addItem(category["CR_Category_Name"], category["CR_Category_Category_ID"])
        except pymysql.Error as e:
            print("Error:", e)

    def update_supplier_id(self, index):
        if index >= 0:  # Ensure a valid index is selected
            # Get the ID corresponding to the selected supplier
            self.supplier_id = self.supplier_combo_box.itemData(index)

    def update_category_id(self, index):
        if index >= 0:  # Ensure a valid index is selected
            # Get the ID corresponding to the selected category
            self.category_id = self.category_combo_box.itemData(index)

    def save_new_product(self):
        # Get product details from the input fields
        product_code = self.get_line_edit_text("Product code:")
        product_name = self.get_line_edit_text("Product name:")
        purchase_price_text = self.get_line_edit_text("Purchase price:")
        selling_price_text = self.get_line_edit_text("Selling price:")
        stock_quantity_text = self.get_line_edit_text("Stock quantity:")
        min_stock_text = self.get_line_edit_text("Minimum stock:")
        max_stock_text = self.get_line_edit_text("Maximum stock:")

        # Validate non-empty fields
        if not all([product_code, product_name, purchase_price_text, selling_price_text,
                    stock_quantity_text, min_stock_text, max_stock_text]):
            QMessageBox.warning(self, "Warning", "Please fill in all required fields.")
            return

        # Convert text inputs to decimal if they are not empty
        try:
            purchase_price = decimal.Decimal(purchase_price_text)
            selling_price = decimal.Decimal(selling_price_text)
        except decimal.InvalidOperation:
            QMessageBox.warning(self, "Error", "Purchase Price and Selling Price must be valid decimal numbers.")
            return

        # Convert text inputs to integers for other fields
        try:
            stock_quantity = int(stock_quantity_text) if stock_quantity_text else None
            min_stock = int(min_stock_text) if min_stock_text else None
            max_stock = int(max_stock_text) if max_stock_text else None
        except ValueError:
            QMessageBox.warning(self, "Error", "Stock Quantity, Min. Stock, and Max. Stock must be valid integers.")
            return

        # Check if supplier and category IDs are set
        if self.supplier_id is None or self.category_id is None:
            QMessageBox.warning(self, "Warning", "Please select a supplier and category.")
            return

        date_in = date.today()

        # Save the new product to the database
        try:
            with self.conn.cursor() as cursor:
                query = ("INSERT INTO Product (CR_Product_ProductCode, CR_Product_Name, CR_Product_Price_B, "
                         "CR_Product_Price_S, CR_Product_Stock_quantity, CR_Product_Min_Stock, CR_Product_Max_Stock, "
                         "CR_Product_Supplier_ID, CR_Product_Category_ID, CR_Product_DateIn) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                cursor.execute(query, (product_code, product_name, purchase_price, selling_price, stock_quantity,
                                       min_stock, max_stock, self.supplier_id, self.category_id, date_in))
                self.conn.commit()

                # Fetch the ID of the newly inserted product
                new_product_id = cursor.lastrowid

                # Fetch details of the newly inserted product
                cursor.execute("""
                    SELECT 
                        p.CR_Product_Product_ID,
                        p.CR_Product_ProductCode,
                        p.CR_Product_Name,
                        p.CR_Product_Price_B,
                        p.CR_Product_Price_S,
                        p.CR_Product_Stock_quantity,
                        p.CR_Product_Min_Stock,
                        p.CR_Product_Max_Stock,
                        s.CR_Supplier_Name,  
                        c.CR_Category_Name,
                        p.CR_Product_DateIn
                    FROM 
                        Product p
                    INNER JOIN 
                        Supplier s ON p.CR_Product_Supplier_ID = s.CR_Supplier_Supplier_ID
                    INNER JOIN 
                        Category c ON p.CR_Product_Category_ID = c.CR_Category_Category_ID
                    WHERE 
                        p.CR_Product_Product_ID = %s
                """, new_product_id)
                new_product = cursor.fetchone()

                # Append the new product to the table
                self.table.setRowCount(self.table.rowCount() + 1)
                for col, field in enumerate(new_product.values()):
                    if col in [0, 1, 2, 3, 4, 8, 9, 10]:  # Read-only columns
                        if col in [0, 3, 4]:  # Numeric fields
                            item = NumericTableWidgetItem(str(field))
                        else:
                            item = QTableWidgetItem(str(field))
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    elif col in [5, 6, 7]:  # Numeric fields
                        item = NumericTableWidgetItem(str(field))
                    else:  # Default for other fields
                        item = QTableWidgetItem(str(field))
                    self.table.setItem(self.table.rowCount() - 1, col, item)

            # Clear input fields after successful save
            for widget in self.new_product_fields_widget.findChildren(QLineEdit):
                widget.clear()

            # Reset supplier and category combo boxes to the first empty item
            self.supplier_combo_box.setCurrentIndex(0)
            self.category_combo_box.setCurrentIndex(0)

            QMessageBox.information(self, "Success", "New product added successfully.")
        except pymysql.Error as e:
            QMessageBox.warning(self, "Error", f"Error saving new product: {str(e)}")

    def get_line_edit_text(self, label_text):
        for i in range(self.new_product_fields.count()):
            layout = self.new_product_fields.itemAt(i)
            if layout is not None and isinstance(layout, QHBoxLayout):
                label = layout.itemAt(1).widget()  # Assuming label is at index 1
                if label.text() == label_text:
                    line_edit = layout.itemAt(2).widget()  # Assuming QLineEdit is at index 2
                    return line_edit.text()
        return ""

    def toggle_product_fields(self):
        # Store the current window state
        current_state = self.windowState()

        if self.new_product_checkbox.isChecked():
            self.new_product_fields_widget.setVisible(True)
            self.btn_save.show()  # Show the save button
        else:
            self.new_product_fields_widget.setVisible(False)
            self.btn_save.hide()  # Hide the save button

        # Restore the window state
        self.setWindowState(current_state)

    def print_products_to_pdf(self):
        try:
            # Custom FPDF class to include header
            class PDF(FPDF):
                def header(self):
                    # Select Arial bold 12
                    self.set_font('Arial', 'B', 12)
                    # Add date and time in top-left corner
                    self.cell(0, 10, 'Product List - Date: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, 'L')
                    # Line break
                    self.ln(20)

            # Set up PDF file with landscape orientation
            pdf = PDF(orientation='L')
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Calculate maximum width available for columns
            page_width = pdf.w - 2 * pdf.l_margin
            num_cols = 11  # Adjust number of columns based on visible columns
            col_widths = [page_width / num_cols] * num_cols

            with self.conn.cursor() as cursor:
                # Fetch all rows from Product table
                cursor.execute("""
                                    SELECT 
                                        p.CR_Product_Product_ID,
                                        p.CR_Product_ProductCode,
                                        p.CR_Product_Name,
                                        p.CR_Product_Price_B,
                                        p.CR_Product_Price_S,
                                        p.CR_Product_Stock_quantity,
                                        p.CR_Product_Min_Stock,
                                        p.CR_Product_Max_Stock,
                                        s.CR_Supplier_Name,
                                        c.CR_Category_Name,
                                        CR_Product_DateIn
                                    FROM 
                                        Product p
                                    INNER JOIN 
                                        Supplier s ON p.CR_Product_Supplier_ID = s.CR_Supplier_Supplier_ID
                                    INNER JOIN 
                                        Category c ON p.CR_Product_Category_ID = c.CR_Category_Category_ID
                                """)
                products = cursor.fetchall()

                # Filter the products based on search input
                search_text = self.search_input.text().strip().lower()
                if search_text:
                    sorted_products = [product for product in products if
                                 any(search_text in str(field).lower() for field in product.values())]
                else:
                    sorted_products = sorted(products, key=lambda x: x['CR_Product_Product_ID'])

                # Set font size and style
                pdf.set_font("Arial", size=8)

                # Add table headers
                headers = ["ID", "Product Code", "Product Name", "Purchase Price", "Selling Price", "Stock Quantity",
                           "Min. Stock", "Max. Stock", "Supplier", "Category", "Date in Stock"]
                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, header, border=1)
                pdf.ln()

                # Add table rows
                for product in sorted_products:
                    for i, field in enumerate(product.values()):
                        # Dynamically adjust font size for name and email fields
                        if i in [2, 8, 9]:  # Index 2 for name, 8 for supplier, 9 for category
                            data = str(field)
                            font_size = 8
                            while pdf.get_string_width(data) > col_widths[i] - 2:
                                font_size -= 0.1
                                pdf.set_font("Arial", size=font_size)
                            pdf.cell(col_widths[i], 8, data, border=1)
                            pdf.set_font("Arial", size=8)  # Reset font size
                        else:
                            pdf.cell(col_widths[i], 8, str(field), border=1)
                    pdf.ln()

            filename, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF files")
            if filename:
                # Append current time to the file name
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                pdf_output_path = f"{filename}_{current_time}.pdf"
                pdf.output(pdf_output_path)

            # Show message box and open the PDF file only if "OK" is clicked
            reply = QMessageBox.information(self, "Success",
                                            f"Product list saved to {pdf_output_path}. Do you want to open it?",
                                            QMessageBox.Ok | QMessageBox.Cancel)
            if reply == QMessageBox.Ok:
                # Open the PDF file after it's saved
                if os.name == 'nt':  # Check if running on Windows
                    os.startfile(pdf_output_path)
                elif os.name == 'posix':  # Check if running on Unix-like system
                    os.system(f"xdg-open {pdf_output_path}")

        except pymysql.Error as e:
            print("Error:", e)

    def save_changes(self):
        try:
            with self.conn.cursor() as cursor:
                for row in range(self.table.rowCount()):
                    product_id = self.table.item(row, 0).text()
                    product_code = self.table.item(row, 1).text()
                    product_name = self.table.item(row, 2).text()
                    purchase_price = self.table.item(row, 3).text()
                    selling_price = self.table.item(row, 4).text()
                    stock_quantity = self.table.item(row, 5).text()
                    min_stock = self.table.item(row, 6).text()
                    max_stock = self.table.item(row, 7).text()

                    supplier_name = self.table.item(row, 8).text()
                    supplier_index = self.supplier_combo_box.findText(supplier_name)
                    supplier_id = self.supplier_combo_box.itemData(supplier_index) if supplier_index != -1 else None

                    category_name = self.table.item(row, 9).text()
                    category_index = self.category_combo_box.findText(category_name)
                    category_id = self.category_combo_box.itemData(category_index) if category_index != -1 else None

                    cursor.execute("""
                                            UPDATE Product 
                                            SET 
                                                CR_Product_ProductCode = %s, 
                                                CR_Product_Name = %s,
                                                CR_Product_Price_B = %s,
                                                CR_Product_Price_S = %s,
                                                CR_Product_Stock_quantity = %s,
                                                CR_Product_Min_Stock = %s,
                                                CR_Product_Max_Stock = %s,
                                                CR_Product_Supplier_ID = %s,
                                                CR_Product_Category_ID = %s
                                            WHERE 
                                                CR_Product_Product_ID = %s
                                        """, (
                        product_code, product_name, purchase_price, selling_price, stock_quantity,
                        min_stock, max_stock, supplier_id, category_id, product_id))

                    # Update the table with the modified data
                    for col, field in enumerate([product_id, product_code, product_name, purchase_price, selling_price,
                                                 stock_quantity, min_stock, max_stock, supplier_name, category_name]):
                        item = self.table.item(row, col)
                        if item:
                            item.setText(str(field))

            self.conn.commit()
            QMessageBox.information(self, "Success", "Changes saved successfully.")
        except pymysql.Error as e:
            print("Error saving changes:", e)
            QMessageBox.warning(self, "Error", "Failed to save changes. Please check the console for more information.")

    def filter_products(self):
        search_text = self.search_input.text().strip().lower()

        for row in range(self.table.rowCount()):
            visible = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    visible = True
                    break
            self.table.setRowHidden(row, not visible)

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

    window = ProductManagementApp()
    window.showMaximized()  # Open window in full-screen mode
    sys.exit(app.exec())