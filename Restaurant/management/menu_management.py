import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
                               QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QTextEdit, QComboBox)
from PySide6.QtCore import QTimer
from pymysql import connect, cursors
from decimal import Decimal

ICON_FOLDER = "../../Icons/"
ITEMS = ["Our Famous", "Greek Burgers", "Loaded Fries", "For the Team", "Kids menu", "Starter Bites", "Siders", "Drinks", "Traditionals"]

class MenuManagement(QWidget):
    def __init__(self):
        """
        Initialize the MenuManagement window for managing menu items.
        """
        super().__init__()
        self.setWindowTitle("Menu Management")
        self.setGeometry(100, 100, 1000, 600)
        self.db_connection = self.create_db_connection()
        self.initUI()
        self.load_menu_items()

    def create_db_connection(self):
        """
        Create and return a database connection.
        """
        return connect(host='localhost', user='dbadmin', password='dbadmin', database='restaurant',
                       cursorclass=cursors.DictCursor)

    def initUI(self):
        """
        Set up the main window's UI elements.
        """
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Columns for ItemID, Name, Description, Price, Category, Update, Delete
        self.table.setHorizontalHeaderLabels(["ItemID", "Name", "Description", "Price", "Category", "Update", "Delete"])
        self.layout.addWidget(self.table)

        # Add menu item form setup
        self.add_item_layout = QHBoxLayout()
        self.name_input = QLineEdit()
        self.description_input = QTextEdit()  # Using QTextEdit for multi-line input
        self.description_input.setFixedSize(300, 60)
        self.price_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(ITEMS)

        self.add_item_button = QPushButton("Add Menu Item")
        self.add_item_button.clicked.connect(self.add_menu_item)

        # Adding widgets to the layout
        self.add_item_layout.addWidget(QLabel("Name:"))
        self.add_item_layout.addWidget(self.name_input)
        self.add_item_layout.addWidget(QLabel("Description:"))
        self.add_item_layout.addWidget(self.description_input)
        self.add_item_layout.addWidget(QLabel("Price:"))
        self.add_item_layout.addWidget(self.price_input)
        self.add_item_layout.addWidget(QLabel("Category:"))
        self.add_item_layout.addWidget(self.category_input)
        self.add_item_layout.addWidget(self.add_item_button)

        self.layout.addLayout(self.add_item_layout)
        self.setLayout(self.layout)
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def load_menu_items(self):
        """
        Load menu items from the database and display them in the table.
        """
        self.table.setRowCount(0)
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM menu_items")
                rows = cursor.fetchall()
                for row_number, row_data in enumerate(rows):
                    self.table.insertRow(row_number)
                    for column_number, key in enumerate(['rs_item_id', 'rs_name', 'rs_description', 'rs_price', 'rs_category']):
                        if key == 'rs_description':  # Description field
                            item = QTableWidgetItem(str(row_data[key]))
                            item.setToolTip(str(row_data[key]))  # Show full description as tooltip
                            self.table.setItem(row_number, column_number, item)
                        elif key == 'rs_price':  # Price field should be formatted as string
                            self.table.setItem(row_number, column_number, QTableWidgetItem(f"{row_data[key]:.2f}"))
                        else:
                            self.table.setItem(row_number, column_number, QTableWidgetItem(str(row_data[key])))
                    self.table.setCellWidget(row_number, 5, self.create_update_button(row_data['rs_item_id']))
                    self.table.setCellWidget(row_number, 6, self.create_delete_button(row_data['rs_item_id']))
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
            print(e)

    def create_update_button(self, itemID):
        """
        Create an update button for a table row.
        """
        btn_update = QPushButton('Update')
        btn_update.clicked.connect(lambda: self.open_update_dialog(itemID))
        return btn_update

    def create_delete_button(self, itemID):
        """
        Create a delete button for a table row.
        """
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.confirm_delete_menu_item(itemID))  # Connect to confirmation method
        return btn_delete

    def confirm_delete_menu_item(self, itemID):
        """
        Confirm deletion of a menu item.
        """
        confirmation = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this menu item?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.delete_menu_item(itemID)

    def add_menu_item(self):
        """
        Add a new menu item to the database.
        """
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        price = self.price_input.text()
        category = self.category_input.currentText()

        if not all([name, description, price, category]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        confirmation = QMessageBox.question(self, "Confirm Action",
                                            "Are you sure you want to add this menu item?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    # Pull the last item of rs_item_id
                    cursor.execute("SELECT COALESCE(MAX(rs_item_id), 0) AS max_id FROM menu_items")
                    result = cursor.fetchone()
                    last_id = result['max_id']
                    new_id = last_id + 1

                    # Insert the new menu item with the new_id
                    cursor.execute(
                        "INSERT INTO menu_items (rs_item_id, rs_name, rs_description, rs_price, rs_category) VALUES (%s, %s, %s, %s, %s)",
                        (new_id, name, description, price, category)
                    )
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Menu item added successfully.")
                    self.load_menu_items()  # Reload menu items

                    # Clear the input fields
                    self.name_input.clear()
                    self.description_input.clear()
                    self.price_input.clear()
                    self.category_input.setCurrentIndex(0)  # Reset to the first category
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "Menu item addition cancelled.")

    def delete_menu_item(self, itemID):
        """
        Delete a menu item from the database.
        """
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("DELETE FROM menu_items WHERE rs_item_id = %s", (int(itemID),))
                self.db_connection.commit()
                QMessageBox.information(self, "Success", "Menu item deleted successfully.")
                self.load_menu_items()  # Reload menu items
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def open_update_dialog(self, itemID):
        """
        Open the update dialog for a menu item.
        """
        dialog = UpdateMenuDialog(itemID, self.db_connection, self)
        if dialog.exec_():  # Check if dialog was accepted (menu item was updated)
            self.load_menu_items()  # Reload menu items

class UpdateMenuDialog(QDialog):
    def __init__(self, itemID, db_connection, parent=None):
        """
        Initialize the UpdateMenuDialog for updating a menu item.
        """
        super().__init__(parent)
        self.itemID = itemID
        self.db_connection = db_connection
        self.setWindowTitle('Update Menu Item')
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        """
        Set up the dialog's UI elements.
        """
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.description_input = QTextEdit()
        self.price_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(ITEMS)

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)
        form_layout.addRow("Price:", self.price_input)
        form_layout.addRow("Category:", self.category_input)

        self.update_button = QPushButton("Update Menu Item")
        self.update_button.clicked.connect(self.update_menu_item)

        layout.addLayout(form_layout)
        layout.addWidget(self.update_button)

        self.load_menu_item_data()

    def load_menu_item_data(self):
        """
        Load existing data for the menu item into the dialog's fields.
        """
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT rs_name, rs_description, rs_price, rs_category FROM menu_items WHERE rs_item_id = %s", (self.itemID,))
                item = cursor.fetchone()
                if item:
                    self.name_input.setText(item['rs_name'])
                    self.description_input.setText(item['rs_description'])
                    self.price_input.setText(str(item['rs_price']))
                    current_category_index = self.category_input.findText(item['rs_category'])
                    if current_category_index >= 0:
                        self.category_input.setCurrentIndex(current_category_index)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load menu item data: {e}")

    def update_menu_item(self):
        """
        Update the menu item in the database.
        """
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        price = self.price_input.text()
        category = self.category_input.currentText()

        if not all([name, description, price, category]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        confirmation = QMessageBox.question(self, "Confirm Action",
                                             "Are you sure you want to update this menu item?",
                                             QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("UPDATE menu_items SET rs_name=%s, rs_description=%s, rs_price=%s, rs_category=%s WHERE rs_item_id=%s",
                                   (name, description, price, category, self.itemID))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Menu item updated successfully.")
                    self.accept()  # Close dialog with accept status
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "Menu item update cancelled.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MenuManagement()
    window.show()
    sys.exit(app.exec())
