from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QLabel, QLineEdit, QCheckBox, QHBoxLayout, QFileDialog
from PySide6.QtGui import QColor, QPalette, QIcon, QPixmap, QGuiApplication
from PySide6.QtCore import Qt
import sys
import os
from fpdf import FPDF
from datetime import datetime
import pymysql
from CreatePostalcode import AddPostalCodeDialog

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

class CustomerManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Customer Management")
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

        # Hide new customer fields initially
        self.new_customer_fields_widget.setVisible(False)

    def init_ui(self):
        self.layout = QVBoxLayout()  # Define QVBoxLayout as instance variable

        # Add checkbox to toggle new customer fields
        self.new_customer_checkbox = QCheckBox("New Customer")
        self.new_customer_checkbox.stateChanged.connect(self.toggle_customer_fields)
        self.layout.addWidget(self.new_customer_checkbox)

        # Add new customer fields layout
        self.new_customer_fields_widget = QWidget()
        self.new_customer_fields = QVBoxLayout(self.new_customer_fields_widget)

        # Base directory where the icons folder is located
        base_dir = windows_base_dir  # Change this to match your base directory on Windows

        # If running on Unix-like system, adjust the base directory
        if os.name == "posix":
            base_dir = fedora_base_dir  # Replace this with the actual path on Unix-like systems

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

        # Add search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search customers...")
        self.search_input.setStyleSheet("color: white;")  # Set font color to white
        self.search_input.textChanged.connect(self.filter_customers)
        self.layout.addWidget(self.search_input)

        # Add table view for customers
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Name", "Email", "Country", "Address", "Postal Code", "City", "Phone Number", "VAT"])
        self.layout.addWidget(self.table)

        # Set sorting enabled for the table
        self.table.setSortingEnabled(True)

        # Connect signal to update city when postal code is edited in the table
        self.table.cellChanged.connect(self.update_city_from_table)

        # Add save button
        self.btn_save_changes = QPushButton("Save Changes")
        self.btn_save_changes.clicked.connect(self.save_changes)
        self.layout.addWidget(self.btn_save_changes)

        # Print Button
        self.btn_print_pdf = QPushButton("Print Customer List to PDF")
        self.btn_print_pdf.clicked.connect(self.print_customers_to_pdf)
        self.layout.addWidget(self.btn_print_pdf)

        # Set layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)


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

    # Slot to handle the newly added postal code and city
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

    def update_city_from_table(self, row, column):
        if column == 5:  # Check if the edited cell is in the postal code column
            postal_code_text = self.table.item(row, column).text()

            try:
                postal_code = int(postal_code_text)

                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT CR_PostalCode_City FROM postalcode WHERE CR_PostalCode_Zipcode = %s",
                                   (postal_code,))
                    city_data = cursor.fetchone()

                if city_data:
                    # Update the corresponding city column
                    city_item = QTableWidgetItem(city_data["CR_PostalCode_City"])
                    city_item.setFlags(city_item.flags() ^ Qt.ItemIsEditable)  # Make city field read-only
                    self.table.setItem(row, 6, city_item)

            except (ValueError, pymysql.Error) as e:
                print("Error:", e)

    def populate_table(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Customer")  # Fetch all rows from Customer table
                customers = cursor.fetchall()

                self.table.setRowCount(len(customers))
                for row, product in enumerate(customers):
                    for col, field in enumerate(product.values()):
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

                        self.table.setItem(row, col, item)
                for row, customer in enumerate(customers):
                    for col, field in enumerate(
                            ["CR_Customer_Customer_ID", "CR_Customer_Name", "CR_Customer_Email",
                             "CR_Customer_Country", "CR_Customer_Address", "CR_Customer_Zipcode",
                             "CR_Customer_City", "CR_Customer_Phone_number", "CR_Customer_VAT"]):
                        if field == "CR_Customer_Customer_ID":
                            item = NumericTableWidgetItem(customer[field])
                        else:
                            item = QTableWidgetItem(str(customer[field]))
                            if field == "CR_Customer_City":
                                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)  # Make city field read-only
                        self.table.setItem(row, col, item)

                # Resize columns to fit content
                self.table.resizeColumnsToContents()

            # Sort the table by ID after populating
            self.table.sortByColumn(0, Qt.AscendingOrder)

        except pymysql.Error as e:
            print("Error:", e)

        # Connect signal to handle cell changes
        self.table.cellChanged.connect(self.handle_cell_changed)

    def handle_cell_changed(self, row, column):
        if column == 5:  # Check if the edited cell is in the postal code column
            postal_code_text = self.table.item(row, column).text()

            try:
                postal_code = int(postal_code_text)

                with self.conn.cursor() as cursor:
                    cursor.execute("SELECT CR_PostalCode_City FROM postalcode WHERE CR_PostalCode_Zipcode = %s",
                                   (postal_code,))
                    city_data = cursor.fetchone()

                if city_data:
                    # Update the corresponding city column
                    city_item = QTableWidgetItem(city_data["CR_PostalCode_City"])
                    city_item.setFlags(city_item.flags() ^ Qt.ItemIsEditable)  # Make city field read-only
                    self.table.setItem(row, 6, city_item)
                else:
                    # If postal code doesn't exist, prompt user to add it
                    reply = QMessageBox.question(self, "Postal Code Not Found",
                                                 "Entered Postal Code does not exist. Do you want to add it?",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        # Open dialog to add new postal code
                        dialog = AddPostalCodeDialog(postal_code_text)  # Pass the postal code to dialog
                        dialog.conn = self.conn  # Assign the database connection
                        dialog.postal_code_saved.connect(self.handle_new_postal_code)  # Connect to signal
                        dialog.exec()

            except (ValueError, pymysql.Error) as e:
                print("Error:", e)

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
            vat = self.get_line_edit_text("VAT:") if self.get_line_edit_text("VAT:") else 'nil'

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
            self.populate_table()
            QMessageBox.information(self, "Success", "New customer added successfully.")
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

    def print_customers_to_pdf(self):
        try:
            # Custom FPDF class to include header
            class PDF(FPDF):
                def header(self):
                    # Select Arial bold 12
                    self.set_font('Arial', 'B', 12)
                    # Add date and time in top-left corner
                    self.cell(0, 10, 'Customer List - Date: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0, 'L')
                    # Line break
                    self.ln(20)

            # Set up PDF file with landscape orientation
            pdf = PDF(orientation='L')
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            # Calculate maximum width available for columns
            page_width = pdf.w - 2 * pdf.l_margin
            num_cols = 9  # Adjust number of columns based on visible columns
            col_widths = [page_width / num_cols] * num_cols

            with self.conn.cursor() as cursor:
                # Fetch all rows from Customer table
                cursor.execute("SELECT * FROM Customer")
                customers = cursor.fetchall()

                # Filter the customers based on search input
                search_text = self.search_input.text().strip().lower()
                if search_text:
                    sorted_customers = [customer for customer in customers if
                                 any(search_text in str(field).lower() for field in customer.values())]
                else:
                    sorted_customers = sorted(customers, key=lambda x: x['CR_Customer_Customer_ID'])

                # Set font size and style
                pdf.set_font("Arial", size=8)

                # Add table headers
                headers = ["ID", "Name", "Email", "Country", "Address", "Postal Code", "City", "Phone Number", "VAT"]
                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, header, border=1)
                pdf.ln()

                # Add table rows
                for customer in sorted_customers:
                    for i, field in enumerate(customer.values()):
                        # Dynamically adjust font size for name and email fields
                        if i in [1, 2, 4, 6]:  # Index 1 for name, 2 for email, 4 for address, 6 for city
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
            if not filename:
                return
            else:
                # Append current time to the file name
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                pdf_output_path = f"{filename}_{current_time}.pdf"
                pdf.output(pdf_output_path)

            # Show message box and open the PDF file only if "OK" is clicked
            reply = QMessageBox.information(self, "Success",
                                            f"Customer list saved to {pdf_output_path}. Do you want to open it?",
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
                    customer_id = self.table.item(row, 0).text()
                    name = self.table.item(row, 1).text()
                    email = self.table.item(row, 2).text()
                    country = self.table.item(row, 3).text()
                    address = self.table.item(row, 4).text()
                    postal_code_text = self.table.item(row, 5).text()
                    phone_number = self.table.item(row, 7).text()
                    vat = self.table.item(row, 8).text() if self.table.item(row, 8).text() else'nil'

                    # Convert postal code to integers, set to 0 if not convertible
                    try:
                        postal_code = int(postal_code_text)
                    except (TypeError, ValueError):
                        postal_code = 0

                    # Fetch city based on postal code
                    with self.conn.cursor() as inner_cursor:
                        inner_cursor.execute(
                            "SELECT CR_PostalCode_City FROM postalcode WHERE CR_PostalCode_Zipcode = %s",
                            (postal_code,))
                        result = inner_cursor.fetchone()
                        city = result["CR_PostalCode_City"] if result else ""

                        # If postal code does not exist, prompt user to add it
                        if not result:
                            reply = QMessageBox.question(self, "Postal Code Not Found",
                                                         f"The postal code {postal_code} does not exist. Do you want to add it?",
                                                         QMessageBox.Yes | QMessageBox.No)
                            if reply == QMessageBox.Yes:
                                dialog = AddPostalCodeDialog(str(postal_code))  # No need to pass any arguments
                                dialog.conn = self.conn  # Assign the database connection
                                dialog.postal_code_saved.connect(self.handle_new_postal_code)  # Connect to signal
                                dialog.exec()
                                # Fetch city again after potential postal code addition
                                inner_cursor.execute(
                                    "SELECT CR_PostalCode_City FROM postalcode WHERE CR_PostalCode_Zipcode = %s",
                                    (postal_code,))
                                result = inner_cursor.fetchone()
                                city = result["CR_PostalCode_City"] if result else ""

                    cursor.execute("""
                        UPDATE Customer 
                        SET 
                            CR_Customer_Name = %s, 
                            CR_Customer_Email = %s,
                            CR_Customer_Country = %s,
                            CR_Customer_Address = %s,
                            CR_Customer_Zipcode = %s,
                            CR_Customer_City = %s,
                            CR_Customer_Phone_number = %s,
                            CR_Customer_VAT = %s
                        WHERE 
                            CR_Customer_Customer_ID = %s
                    """, (
                        name, email, country, address, postal_code, city, phone_number, vat, customer_id))
            self.conn.commit()
            self.populate_table()
            QMessageBox.information(self, "Success", "Changes saved successfully.")
        except pymysql.Error as e:
            print("Error saving changes:", e)
            QMessageBox.warning(self, "Error", "Failed to save changes. Please check the console for more information.")

    def filter_customers(self):
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

    window = CustomerManagementApp()
    window.showMaximized()  # Open window in full-screen mode
    sys.exit(app.exec())