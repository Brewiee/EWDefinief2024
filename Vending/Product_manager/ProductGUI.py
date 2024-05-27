import sys
import pymysql
import os
from src.Vending_UI.Product_manager.class_product_interface import product_interface
from src.Vending_UI.Product_manager.class_highlightdelegate import HighlightDelegate
from src.Vending_UI.Log_creator.class_custom_logger import CustomLogger
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, \
     QInputDialog, QLineEdit, QMessageBox, QWidget, QTreeWidgetItem, QTreeWidget, \
    QHeaderView, QGridLayout, QCompleter, QAbstractItemView
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon


class ProductGUI(QMainWindow):
    """Class representing the Product CRUD Interface."""

    def __init__(self):
        """Initialize the ProductGUI instance."""
        super().__init__()
        self.setWindowTitle("Product Interface")
        self.setGeometry(100, 100, 1920, 1080)

        self.product_interface = product_interface()
        self.logger = CustomLogger("Product_GUI", "Logging")
        self.logger.log_error("Start Product GUI Error Log")

        # Define input layout attribute
        self.input_layout = None

        self.create_widgets()

        # Read the products immediately upon starting the GUI
        self.read_products()

        # Flag to indicate whether a change has occurred since the last refresh
        self.change_occurred = False

        # Flag to track whether the Save button is connected
        self.save_button_connected = False

        # Connect double-click event to on_double_click method
        self.tree.itemDoubleClicked.connect(self.on_double_click)

    def create_widgets(self):
        """Create the widgets for the GUI."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create buttons layout
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        # Get the path to the data directory
        data_dir = os.path.join(os.getcwd(), 'data')

        # Construct the path to the Icons directory within the data directory
        icons_dir = os.path.join(data_dir, 'Icons')

        # Define button data with icon file paths
        button_data = [
            ("Create Product", self.toggle_input_fields, os.path.join(icons_dir, "create_icon.png")),
            ("Update Product", self.update_product, os.path.join(icons_dir, "update_icon.png")),
            ("Delete Product", self.delete_product, os.path.join(icons_dir, "delete_icon.png")),
            ("Quit", QApplication.instance().quit, os.path.join(icons_dir, "quit_icon.png"))
        ]

        for text, handler, icon_path in button_data:
            button = QPushButton(text)
            icon = QIcon(icon_path)
            button.setIcon(icon)
            button.setIconSize(icon.actualSize(QSize(24, 24)))  # Adjust icon size if needed
            button.clicked.connect(handler)

            # Set button text alignment
            button.setStyleSheet("text-align:left;")

            buttons_layout.addWidget(button)

        # Create input fields layout
        self.input_layout = QGridLayout()  # Define input layout attribute
        main_layout.addLayout(self.input_layout)
        self.input_layout.setColumnStretch(1, 1)  # Allow input fields to expand

        # Create search field with autocomplete functionality
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("Search for a product name...")
        main_layout.addWidget(self.search_entry)
        self.setup_autocomplete()  # Set up autocomplete for the search field

        # Create input fields layout
        input_layout = QGridLayout()
        main_layout.addLayout(input_layout)
        input_layout.setColumnStretch(1, 1)  # Allow input fields to expand

        # Product code
        self.code_label = QLabel("Product Code:")
        input_layout.addWidget(self.code_label, 0, 0)
        self.code_entry = QLineEdit()
        self.code_entry.setPlaceholderText("Enter product code")
        input_layout.addWidget(self.code_entry, 0, 1)

        # Product name
        self.name_label = QLabel("Product Name:")
        input_layout.addWidget(self.name_label, 1, 0)
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("Enter product name")  # Set placeholder text
        input_layout.addWidget(self.name_entry, 1, 1)

        # Product price
        self.price_label = QLabel("Product Price:")
        input_layout.addWidget(self.price_label, 2, 0)
        self.price_entry = QLineEdit()
        self.price_entry.setPlaceholderText("Enter product price")  # Set placeholder text
        input_layout.addWidget(self.price_entry, 2, 1)

        # Product VAT
        self.tax_label = QLabel("Product VAT:")
        input_layout.addWidget(self.tax_label, 3, 0)
        self.tax_entry = QLineEdit()
        self.tax_entry.setPlaceholderText("Enter product VAT")  # Set placeholder text
        input_layout.addWidget(self.tax_entry, 3, 1)

        # Save button
        self.save_button = QPushButton("Save")
        input_layout.addWidget(self.save_button, 4, 0, 1, 2)  # Span button across two columns
        self.save_button.clicked.connect(self.save_updated_product)

        # Create TreeWidget
        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)  # Increase column count to include "Tax"
        self.tree.setHeaderLabels(["ID", "Code", "Name", "Price", "VAT"])  # Adjust header labels
        main_layout.addWidget(self.tree)

        # Stretch the last section of the header to fill the remaining space
        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Initially hide input fields
        self.hide_input_fields()

        # Set up delegate for custom item painting
        self.tree.setItemDelegate(HighlightDelegate())

    def read_products(self):
        """
        Read products from the database and populate the TreeWidget.
        """
        try:
            products = self.product_interface.read_products()
            for product in products:
                item = QTreeWidgetItem(map(str, product))
                self.tree.addTopLevelItem(item)
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "Database Error", f"Error accessing database: {e}")
            self.logger.log_error(f"Database Error, error accessing database: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            self.logger.log_error(f"Error: An unexpected error occured: {e}")

    def toggle_input_fields(self):
        """Toggle the visibility of input fields."""
        if self.code_label.isHidden():
            self.create_product()  # Directly call create_product method
        else:
            self.hide_input_fields()

    def show_input_fields(self):
        """Show input fields."""
        self.code_label.show()
        self.code_entry.show()
        self.name_label.show()
        self.name_entry.show()
        self.price_label.show()
        self.price_entry.show()
        self.tax_label.show()
        self.tax_entry.show()
        self.save_button.show()  # Show the "Save" button
        self.save_button.clicked.connect(self.save_updated_product)  # Connect "Save" button to save_updated_product

    def hide_input_fields(self):
        """Hide input fields."""
        self.code_label.hide()
        self.code_entry.hide()
        self.name_label.hide()
        self.name_entry.hide()
        self.price_label.hide()
        self.price_entry.hide()
        self.tax_label.hide()
        self.tax_entry.hide()
        self.save_button.hide()  # Hide the "Save" button
        self.save_button.clicked.disconnect()  # Disconnect "Save" button from save_updated_product

    def hide_and_empty_input_fields(self):
        """Hide and empty input fields."""
        self.code_entry.clear()
        self.name_entry.clear()
        self.price_entry.clear()
        self.tax_entry.clear()
        self.hide_input_fields()

    def save_product(self):
        """Save the product using the entered details."""
        product_code = self.code_entry.text()
        product_name = self.name_entry.text()
        product_price = float(self.price_entry.text())
        product_tax = float(self.tax_entry.text())

        # Create the product using the product interface
        self.product_interface.create_product(product_code, product_name, product_price, product_tax)
        formatted_price = "{:.2f}".format(product_price)  # Format price to 2 decimal places
        QMessageBox.information(self, "Success", "Product created successfully!")
        self.change_occurred = True  # Set the flag to indicate a change
        self.refresh_products()  # Refresh the products list
        self.hide_and_empty_input_fields()  # Hide and empty input fields after saving

    def refresh_products(self):
        """Refresh the product list displayed in the TreeWidget."""
        self.tree.clear()

        try:
            products = self.product_interface.read_products()
            for product in products:
                item = QTreeWidgetItem(map(str, product))
                self.tree.addTopLevelItem(item)
            self.change_occurred = False  # Reset the flag after refreshing
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "Database Error", f"Error accessing database: {e}")
            self.logger.log_error(f"Database Error, error accessing database: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            self.logger.log_error(f"Error: An unexpected error occured: {e}")

    def create_product(self):
        """
        Create a new product using input fields and update the product list.
        """
        # Ensure input fields are visible
        self.show_input_fields()

        # Clear existing input field values
        self.code_entry.clear()
        self.name_entry.clear()
        self.price_entry.clear()
        self.tax_entry.clear()

        # Change the button text to "Save"
        self.save_button.setText("Save")

        # Connect the Save button to the save_product method
        self.save_button.clicked.disconnect()  # Disconnect any existing connections
        self.save_button.clicked.connect(self.save_product)  # Connect to save_product method

    def update_product(self):
        """Update an existing product."""
        if self.code_label.isHidden():
            # If input fields are hidden, show them to update a product
            self.toggle_input_fields()
            self.save_button.setText("Save")  # Change the button text to "Save"
            # Connect the save button to save_updated_product method
            self.save_button.clicked.disconnect()  # Disconnect any existing connections
            # Connect the save button to save_updated_product method with product_id as argument
            self.save_button.clicked.connect(lambda: self.save_updated_product(product_id))

            # Prompt user for product ID to update
            product_id, ok = QInputDialog.getInt(self, "Update Product", "Enter product ID to update:")
            if ok:
                try:
                    current_code = None  # Initialize current_code variable
                    current_name = None
                    current_price = None
                    current_tax = None

                    # Fetch all products
                    products = self.product_interface.read_products()

                    # Iterate through products to find the one with the given ID
                    for product in products:
                        if product[0] == product_id:  # Assuming ID is the first element of each product tuple
                            current_code = product[1]  # Assuming Code is the second element
                            current_name = product[2]  # Assuming Name is the third element
                            current_price = product[3]  # Assuming Price is the fourth element
                            current_tax = product[4]  # Assuming Tax is the fifth element

                            break  # Stop searching once the product is found

                    if current_name is not None and current_price is not None:
                        # Fill input fields with current product details
                        self.code_entry.setText(str(current_code))  # Populate code entry with product code
                        self.name_entry.setText(current_name)
                        self.price_entry.setText(str(current_price))
                        self.tax_entry.setText(str(current_tax))
                    else:
                        QMessageBox.critical(self, "Error", "Product not found.")
                        self.logger.log_error(f"Error: Product id {product_id} not found ")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error retrieving product details: {e}")
                    self.logger.log_error(f"Error retrieving product details: {e}")
        else:
            # If input fields are visible, hide them
            self.hide_input_fields()

    def save_updated_product(self, product_id):
        """Save updated product information."""
        print(product_id)
        new_product_code = self.code_entry.text()  # Assign product code input to new_product_code
        print(new_product_code)
        new_name = self.name_entry.text()  # Assign product name input to new_name
        print(new_name)
        new_price = float(self.price_entry.text())
        print(new_price)
        new_tax = float(self.tax_entry.text())
        print(new_tax)
        try:
            # Update the product with new name, price, and tax
            self.product_interface.update_product(product_id, new_product_code, new_name, new_price, new_tax)
            QMessageBox.information(self, "Success", "Product updated successfully!")
            self.refresh_products()  # Refresh the products list

            # Hide and empty input fields
            self.hide_and_empty_input_fields()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error updating product: {e}")
            self.logger.log_error(f"Error updating product {e}")

    def delete_product(self):
        """Delete the selected product after confirmation and refresh the product list."""
        # Similar to update_product, use QInputDialog to get product ID

        # Get the selected item from the TreeWidget
        selected_item = self.tree.currentItem()

        # Check if any item is selected
        if selected_item:
            # Get the values of the selected item
            values = [selected_item.text(column) for column in range(self.tree.columnCount())]
            if values:
                product_id = int(values[0])  # Assuming ID is the first column
                product_name = values[2]  # Assuming Name is the third column

                # Ask for confirmation before deleting the product
                confirm = QMessageBox.question(self, "Confirmation",
                                                f"Are you sure you want to delete the product '{product_name}'?",
                                                QMessageBox.Yes | QMessageBox.No)
                if confirm == QMessageBox.Yes:
                    try:
                        self.product_interface.delete_product(product_id)
                        QMessageBox.information(self, "Success", "Product deleted successfully!")
                        self.change_occurred = True  # Set the flag to indicate a change
                        self.refresh_products()  # Refresh the products list
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Error deleting product: {e}")
                        self.logger.log_error(f"Error deleting product: {e}")
            else:
                QMessageBox.information(self, "Info", "Please select a product to delete.")
        else:
            QMessageBox.information(self, "Info", "Please select a product to delete.")

    def on_double_click(self, event):
        """
        Handle double-click event on a product in the Treeview.
        """
        # Get the selected item from the TreeWidget
        selected_item = self.tree.currentItem()

        # Check if any item is selected
        if selected_item:
            # Get the product ID from the selected item
            product_id_text = selected_item.text(0)  # Assuming ID is the first column
            try:
                product_id = int(product_id_text)
            except ValueError:
                return  # Exit the method if the product ID is invalid

            # Get the values of the selected item
            values = [selected_item.text(column) for column in range(self.tree.columnCount())]
            if values:
                product_name = values[2]  # Assuming Name is the third column
                product_price = float(values[3])  # Assuming Price is the fourth column
                product_tax = int(values[4])  # Assuming Tax is the fifth column

                # Fill input fields with current product details
                self.code_entry.setText(values[1])  # Assuming product code is in the second column
                self.name_entry.setText(product_name)
                self.price_entry.setText(str(product_price))
                self.tax_entry.setText(str(product_tax))

                # Show input fields
                self.show_input_fields()

                # Change the button text to "Save"
                self.save_button.setText("Save")

                # Disconnect the Save button if it's connected
                if self.save_button_connected:
                    self.save_button.clicked.disconnect()
                    self.save_button_connected = False

                # Connect to save method
                self.save_button.clicked.connect(
                    lambda: self.save_updated_product(product_id))
                self.save_button_connected = True

                # Disconnect any existing connections to avoid multiple connections
                self.save_button.clicked.disconnect()

                # Connect to save method
                self.save_button.clicked.connect(
                    lambda: self.save_updated_product(product_id))

                # Ensure product ID is updated synchronously before proceeding
                QApplication.processEvents()
        else:
            QMessageBox.information(self, "Info", "Please select a product to update.")

    def setup_autocomplete(self):
        """Set up autocomplete for the search field."""
        products = self.product_interface.read_products()
        product_names = [product[2] for product in products]  # Assuming Name is the third element
        completer = QCompleter(product_names)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.activated.connect(self.select_product_in_treeview)
        self.search_entry.setCompleter(completer)
        self.search_entry.textChanged.connect(self.filter_products)

    def filter_products(self, text):
        """Filter products in the treeview based on the entered text."""
        if text:
            items = self.tree.findItems(text, Qt.MatchContains | Qt.MatchRecursive, column=2)  # Search by product name
            for item in self.tree.findItems("", Qt.MatchWildcard, column=2):  # Hide all items first
                item.setHidden(True)
            for item in items:
                item.setHidden(False)
        else:
            for item in self.tree.findItems("", Qt.MatchContains | Qt.MatchRecursive, column=2):
                item.setHidden(False)

    def select_product_in_treeview(self, text):
        """Select the corresponding product item in the treeview."""
        items = self.tree.findItems(text, Qt.MatchExactly | Qt.MatchRecursive, column=2)  # Search by product name
        if items:
            item = items[0]  # Take the first matching item
            index = self.tree.indexFromItem(item)
            if index.isValid():
                self.tree.clearSelection()  # Clear previous selection
                self.tree.setCurrentIndex(index)  # Set current index to highlight the item
                self.tree.scrollTo(index, QAbstractItemView.PositionAtCenter)  # Scroll to the selected item


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ProductGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()