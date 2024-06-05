import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QSpinBox, QMessageBox, QGridLayout)
from PySide6.QtCore import QDateTime, Signal
from PySide6.QtGui import QIcon
from pymysql import connect, cursors
from functools import partial

ICON_FOLDER = "../../Icons/"

class CreateOrder(QMainWindow):
    # Signal to indicate that the order has been placed
    about_to_close = Signal()

    def __init__(self, connection, table_number, status, user):
        """
        Initialize the CreateOrder window with the given database connection, table number, and status.
        """
        super().__init__()
        self.setWindowTitle("Create Order")
        self.setGeometry(100, 100, 800, 600)
        self.db_connection = connection
        self.table_number = table_number
        self.user_id = user
        self.status = status
        self.initUI()

    def initUI(self):
        """
        Set up the main window's UI elements.
        """
        widget = QWidget()
        layout = QHBoxLayout()

        self.main_layout = QGridLayout()
        layout.addLayout(self.main_layout)

        self.order_items = QTableWidget(0, 4)
        self.order_items.setHorizontalHeaderLabels(['Name', 'Amount', 'Price', 'Subtotal'])
        layout.addWidget(self.order_items)

        self.place_order_button = QPushButton("Place Order")
        self.place_order_button.setFixedSize(100, 100)
        self.place_order_button.clicked.connect(self.place_order_prompt)  # Connect to place_order_prompt
        layout.addWidget(self.place_order_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Display menu items when the window is initialized
        self.display_categories()
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def display_categories(self):
        """
        Display menu categories as buttons.
        """
        # Clear main layout before loading new items
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

        if self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT rs_category FROM menu_items")
                categories = cursor.fetchall()
                colors = ['#49AEE1', '#5EA508', '#95E534', '#DAF7A6', '#FFC300', '#B87060', '#FF5733', '#C70039', '#581845']
                for index, (category, color) in enumerate(zip(categories, colors)):
                    btn = QPushButton(category['rs_category'])
                    btn.setFixedSize(200, 50)
                    btn.setStyleSheet(f"background-color: {color}; color: black; font-weight: bold;")
                    btn.clicked.connect(partial(self.load_items_by_category, category['rs_category'], clr=color))
                    self.main_layout.addWidget(btn, index, 0)

    def load_items_by_category(self, category, clr):
        """
        Load menu items for the selected category and display them as buttons.
        """
        # Clear main layout before loading new items
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

        # Add a back button
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.display_categories)
        self.main_layout.addWidget(back_btn, 0, 0)

        if self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM menu_items WHERE rs_category = %s", (category,))
                items = cursor.fetchall()
                for index, item in enumerate(items, start=1):
                    btn = QPushButton(item['rs_name'])
                    btn.setFixedSize(200, 50)
                    btn.setStyleSheet(f"background-color: {clr}; color: black; font-weight: bold;")
                    btn.clicked.connect(partial(self.add_item_to_order, item))
                    self.main_layout.addWidget(btn, index, 0)

    def add_item_to_order(self, item):
        """
        Add the selected menu item to the order.
        """
        row_count = self.order_items.rowCount()
        self.order_items.insertRow(row_count)
        self.order_items.setItem(row_count, 0, QTableWidgetItem(item['rs_name']))
        quantity_spin_box = QSpinBox()
        quantity_spin_box.setMinimum(0)
        quantity_spin_box.setValue(1)
        self.order_items.setCellWidget(row_count, 1, quantity_spin_box)
        price = float(item['rs_price'])
        self.order_items.setItem(row_count, 2, QTableWidgetItem(f"{price:.2f}"))

        # Correctly use partial to pass extra arguments (row_count and spin_box itself)
        quantity_spin_box.valueChanged.connect(partial(self.update_subtotal, row_count, quantity_spin_box))

    def update_subtotal(self, row, spin_box, value):
        """
        Update the subtotal when the quantity changes.
        """
        price = float(self.order_items.item(row, 2).text())
        subtotal = value * price  # Use 'value', which is the new spin box value
        self.order_items.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))

    def place_order_prompt(self):
        """
        Display a confirmation prompt before placing the order.
        """
        if self.order_items.rowCount() == 0:
            QMessageBox.warning(self, "Empty Order", "Please add items to the order before placing it.")
            return

        msgBox = QMessageBox()
        msgBox.setText("Are you sure you want to place the order?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec()
        if ret == QMessageBox.Yes:
            self.place_order()
            # Emit the signal
            self.about_to_close.emit()

    def place_order(self):
        """
        Place the order and update the database.
        """
        if not self.table_number or self.table_number == "":
            QMessageBox.warning(self, "Input Error", "Please select a table number.")
            return
        try:
            with self.db_connection.cursor() as cursor:
                # Fetch the table id based on the table number
                cursor.execute("SELECT rs_table_id FROM tables WHERE rs_number = %s", (self.table_number,))
                table = cursor.fetchone()
                if not table:
                    QMessageBox.warning(self, "Error", "Table number does not exist.")
                    return

                table_id = table['rs_table_id']
                order_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
                status = 'Placed'  # Default status, modify as needed
                cursor.execute(
                    "INSERT INTO orders (rs_table_number, rs_user_id, rs_order_time, rs_status) VALUES (%s, %s, %s, %s)",
                    (self.table_number, self.user_id, order_time, status))
                order_id = cursor.lastrowid  # Get the ID of the new order
                cursor.execute("UPDATE tables SET rs_status = 'occupied' WHERE rs_table_id = %s", (table_id,))

                # Insert each item into the orderdetails table
                for row in range(self.order_items.rowCount()):
                    item_name = self.order_items.item(row, 0).text()
                    cursor.execute("SELECT rs_item_id, rs_price FROM menu_items WHERE rs_name = %s", (item_name,))
                    item = cursor.fetchone()
                    if item:
                        quantity = self.order_items.cellWidget(row, 1).value()
                        subtotal = quantity * item['rs_price']
                        cursor.execute(
                            "INSERT INTO orderdetails (rs_order_id, rs_item_id, rs_quantity, rs_subtotal) VALUES (%s, %s, %s, %s)",
                            (order_id, item['rs_item_id'], quantity, subtotal)
                        )

                # Commit the transaction
                self.db_connection.commit()
                self.about_to_close.emit()  # Emit the orderPlaced signal
                self.close()  # Close the window after placing the order
                QMessageBox.information(self, "Success", "Order has been placed successfully.")
        except Exception as e:
            self.db_connection.rollback()  # Rollback in case of any error
            QMessageBox.warning(self, "Database Error", f"An error occurred while placing the order: {e}")
            print(f"An error occurred while placing the order: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainMenu = CreateOrder(connection=None, table_number="", status="", user="")  # Pass appropriate arguments here
    mainMenu.show()
    sys.exit(app.exec())
