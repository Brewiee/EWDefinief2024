import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QTableWidget, \
    QTableWidgetItem, QSpinBox, QMessageBox, QGridLayout
from PySide6.QtCore import Signal, QDateTime
from pymysql import connect, cursors
from functools import partial


class UpdateOrder(QMainWindow):
    orderUpdated = Signal()

    def __init__(self, connection, table_number, status):
        super().__init__()
        self.setWindowTitle("Update Order")
        self.setGeometry(100, 100, 800, 600)
        self.db_connection = connection
        self.table_number = table_number
        self.status = status
        self.current_order_id = None
        self.initUI()

    def initUI(self):
        widget = QWidget()
        layout = QHBoxLayout()

        self.main_layout = QGridLayout()
        layout.addLayout(self.main_layout)

        self.order_items = QTableWidget(0, 4)
        self.order_items.setHorizontalHeaderLabels(['Name', 'Amount', 'Price', 'Subtotal'])
        layout.addWidget(self.order_items)

        self.place_order_button = QPushButton("Update Order")
        self.place_order_button.clicked.connect(self.update_order_prompt)
        layout.addWidget(self.place_order_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.display_categories()
        self.select_and_load_existing_order()

    def display_categories(self):
        # Clear main layout before loading new items
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

        if self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT DISTINCT Category FROM menuitems")
                categories = cursor.fetchall()
                colors = ['#49AEE1', '#5EA508', '#95E534', '#DAF7A6', '#FFC300', '#B87060', '#FF5733', '#C70039',
                          '#581845']  # List of different colors
                for index, (category, color) in enumerate(zip(categories, colors)):
                    btn = QPushButton(category['Category'])
                    btn.setFixedSize(200, 50)
                    btn.setStyleSheet(
                        f"background-color: {color}; color: black; font-weight: bold;")  # Set background color
                    btn.clicked.connect(partial(self.load_items_by_category, category['Category'], clr=color))
                    self.main_layout.addWidget(btn, index, 0)

    def load_items_by_category(self, category, clr):
        for i in reversed(range(self.main_layout.count())):
            self.main_layout.itemAt(i).widget().setParent(None)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.display_categories)
        self.main_layout.addWidget(back_btn, 0, 0)

        if self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM menuitems WHERE Category = %s", (category,))
                items = cursor.fetchall()
                for index, item in enumerate(items, start=1):
                    btn = QPushButton(item['Name'])
                    btn.setFixedSize(200, 50)
                    btn.setStyleSheet(f"background-color: {clr}; color: black; font-weight: bold;")
                    btn.clicked.connect(partial(self.add_item_to_order, item))
                    self.main_layout.addWidget(btn, index, 0)

    def select_and_load_existing_order(self):
        if self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT OrderID FROM orders WHERE TableNumber = %s AND Status = 'placed'",
                               (self.table_number,))
                existing_orders = cursor.fetchall()
                if existing_orders:
                    self.current_order_id = existing_orders[-1]['OrderID']
                    self.load_existing_order_items()

    def load_existing_order_items(self):
        if self.current_order_id and self.db_connection:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT mi.Name, od.Quantity, mi.Price FROM orderdetails od JOIN menuitems mi ON od.ItemID = mi.ItemID WHERE od.OrderID = %s",
                    (self.current_order_id,))
                items = cursor.fetchall()
                for item in items:
                    self.add_existing_item_to_order(item)

    def add_item_to_order(self, item):
        row_count = self.order_items.rowCount()
        self.order_items.insertRow(row_count)
        self.order_items.setItem(row_count, 0, QTableWidgetItem(item['Name']))
        quantity_spin_box = QSpinBox()
        quantity_spin_box.setMinimum(0)
        quantity_spin_box.setValue(1)
        self.order_items.setCellWidget(row_count, 1, quantity_spin_box)
        price = float(item['Price'])
        self.order_items.setItem(row_count, 2, QTableWidgetItem(f"{price:.2f}"))

        # Correctly use partial to pass extra arguments (row_count and spin_box itself)
        quantity_spin_box.valueChanged.connect(partial(self.update_subtotal, row_count, quantity_spin_box))

    def add_existing_item_to_order(self, item):
        row_count = self.order_items.rowCount()
        self.order_items.insertRow(row_count)
        self.order_items.setItem(row_count, 0, QTableWidgetItem(item['Name']))
        quantity_spin_box = QSpinBox()
        quantity_spin_box.setEnabled(False)  # Disable spin box for existing items
        quantity_spin_box.setMinimum(1)
        quantity_spin_box.setValue(item['Quantity'])
        self.order_items.setCellWidget(row_count, 1, quantity_spin_box)
        price = float(item['Price'])
        self.order_items.setItem(row_count, 2, QTableWidgetItem(f"{price:.2f}"))
        subtotal = item['Quantity'] * price
        self.order_items.setItem(row_count, 3, QTableWidgetItem(f"{subtotal:.2f}"))

    def update_subtotal(self, row, spin_box, value):
        # 'value' is the new value of the spin box, automatically passed by the valueChanged signal
        price = float(self.order_items.item(row, 2).text())
        subtotal = value * price  # Use 'value', which is the new spin box value
        self.order_items.setItem(row, 3, QTableWidgetItem(f"{subtotal:.2f}"))

    def update_order_prompt(self):
        # Check if there are items in the order
        if self.order_items.rowCount() == 0:
            QMessageBox.warning(self, "Empty Order", "Please add items to the order before updating it.")
            return

        # Display a dialog for confirmation
        msgBox = QMessageBox()
        msgBox.setText("Are you sure you want to update the order?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            self.update_order()

    def update_order(self):
        if not self.current_order_id:
            QMessageBox.warning(self, "Order Error", "No existing order to update.")
            return
        try:
            with self.db_connection.cursor() as cursor:
                for row in range(self.order_items.rowCount()):
                    item_name = self.order_items.item(row, 0).text()
                    cursor.execute("SELECT ItemID, Price FROM menuitems WHERE Name = %s", (item_name,))
                    item = cursor.fetchone()
                    if item:
                        quantity_spin_box = self.order_items.cellWidget(row, 1)
                        if quantity_spin_box.isEnabled():  # Check if spin box is enabled (new item)
                            quantity = quantity_spin_box.value()
                            subtotal = quantity * item['Price']
                            cursor.execute(
                                "INSERT INTO orderdetails (OrderID, ItemID, Quantity, Subtotal) VALUES (%s, %s, %s, %s)",
                                (self.current_order_id, item['ItemID'], quantity, subtotal))
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
    mainMenu = UpdateOrder()
    mainMenu.show()
    sys.exit(app.exec())
