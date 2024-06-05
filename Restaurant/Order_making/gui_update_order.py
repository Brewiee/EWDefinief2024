import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QSpinBox, QMessageBox, QGridLayout)
from PySide6.QtCore import Signal, QDateTime
from pymysql import connect, cursors
from functools import partial

ICON_FOLDER = "./Icons/"

class UpdateOrder(QMainWindow):
    # Signal to indicate that the order has been updated
    orderUpdated = Signal()

    def __init__(self, connection, table_number, status):
        """
        Initialize the UpdateOrder window with the given database connection, table number, and status.
        """
        super().__init__()
        self.setWindowTitle("Update Order")
        self.setGeometry(100, 100, 1200, 600)
        self.db_connection = connection
        self.table_number = table_number
        self.status = status
        self.current_order_id = None
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

        self.order_items.setColumnWidth(0, 575)  # Name column
        self.order_items.setColumnWidth(1, 100)  # Amount column
        self.order_items.setColumnWidth(2, 100)  # Price column
        self.order_items.setColumnWidth(3, 100)  # Subtotal column

        self.place_order_button = QPushButton("Update Order")
        self.place_order_button.clicked.connect(self.update_order_prompt)
        layout.addWidget(self.place_order_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.display_categories()
        self.select_and_load_existing_order()
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
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

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

    def select_and_load_existing_order(self):
        """
        Select and load the most recent existing order for the table.
        """
        if self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT rs_order_id FROM orders WHERE rs_table_number = %s AND rs_status = 'Placed'",
                               (self.table_number,))
                existing_orders = cursor.fetchall()
                if existing_orders:
                    self.current_order_id = existing_orders[-1]['rs_order_id']
                    self.load_existing_order_items()

    def load_existing_order_items(self):
        """
        Load existing items for the current order and add them to the order table.
        """
        if self.current_order_id and self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("""
                    SELECT mi.rs_name, od.rs_quantity, mi.rs_price
                    FROM orderdetails od
                    JOIN menu_items mi ON od.rs_item_id = mi.rs_item_id
                    WHERE od.rs_order_id = %s
                """, (self.current_order_id,))
                items = cursor.fetchall()

                # Dictionary to consolidate items
                consolidated_items = {}
                for item in items:
                    if item['rs_name'] in consolidated_items:
                        consolidated_items[item['rs_name']]['rs_quantity'] += item['rs_quantity']
                    else:
                        consolidated_items[item['rs_name']] = {
                            'rs_name': item['rs_name'],
                            'rs_quantity': item['rs_quantity'],
                            'rs_price': item['rs_price']
                        }

                for item in consolidated_items.values():
                    self.add_existing_item_to_order(item)

    def add_item_to_order(self, item):
        """
        Add a new item to the order table.
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

    def add_existing_item_to_order(self, item):
        """
        Add an existing item to the order table.
        """
        row_count = self.order_items.rowCount()
        self.order_items.insertRow(row_count)
        self.order_items.setItem(row_count, 0, QTableWidgetItem(item['rs_name']))
        quantity_spin_box = QSpinBox()
        quantity_spin_box.setEnabled(False)  # Disable spin box for existing items
        quantity_spin_box.setMinimum(1)
        quantity_spin_box.setValue(item['rs_quantity'])
        self.order_items.setCellWidget(row_count, 1, quantity_spin_box)
        price = float(item['rs_price'])
        self.order_items.setItem(row_count, 2, QTableWidgetItem(f"{price:.2f}"))
        subtotal = item['rs_quantity'] * price
        self.order_items.setItem(row_count, 3, QTableWidgetItem(f"{subtotal:.2f}"))

    def update_subtotal(self, row, spin_box, value):
        """
        Update the subtotal when the quantity changes.
        """
        price = float(self.order_items.item(row, 2).text())
        subtotal = value * price  # Use 'value', which is the new spin box value
        self.order_items.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))

    def update_order_prompt(self):
        """
        Display a confirmation prompt before updating the order.
        """
        if self.order_items.rowCount() == 0:
            QMessageBox.warning(self, "Empty Order", "Please add items to the order before updating it.")
            return

        msgBox = QMessageBox()
        msgBox.setText("Are you sure you want to update the order?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec()
        if ret == QMessageBox.Yes:
            self.update_order()

    def update_order(self):
        """
        Update the order and save changes to the database.
        """
        if not self.current_order_id:
            QMessageBox.warning(self, "Order Error", "No existing order to update.")
            return
        try:
            with self.db_connection.cursor() as cursor:
                for row in range(self.order_items.rowCount()):
                    item_name = self.order_items.item(row, 0).text()
                    cursor.execute("SELECT rs_item_id, rs_price FROM menu_items WHERE rs_name = %s", (item_name,))
                    item = cursor.fetchone()
                    if item:
                        quantity_spin_box = self.order_items.cellWidget(row, 1)
                        if quantity_spin_box.isEnabled():  # Check if spin box is enabled (new item)
                            quantity = quantity_spin_box.value()
                            subtotal = quantity * item['rs_price']
                            cursor.execute(
                                "INSERT INTO orderdetails (rs_order_id, rs_item_id, rs_quantity, rs_subtotal) VALUES (%s, %s, %s, %s)",
                                (self.current_order_id, item['rs_item_id'], quantity, subtotal))
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Order has been updated successfully.")
            self.orderUpdated.emit()
            self.close()
        except Exception as e:
            self.db_connection.rollback()
            QMessageBox.warning(self, "Database Error", f"An error occurred while updating the order: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    mainMenu = UpdateOrder(connection=None, table_number="", status="")  # Pass appropriate arguments here
    mainMenu.show()
    sys.exit(app.exec())
