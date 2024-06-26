import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                               QMessageBox, QPushButton, QLineEdit, QLabel, QComboBox, QDialog, QFormLayout)
from PySide6.QtCore import QDateTime
from pymysql import connect, cursors

ICON_FOLDER = "../Icons/"

class OrderManagement(QWidget):
    def __init__(self):
        """
        Initialize the OrderManagement window for managing orders.
        """
        super().__init__()
        self.setWindowTitle("Order Management")
        self.setGeometry(100, 100, 1200, 600)
        self.db_connection = self.create_db_connection()
        self.initUI()
        self.load_orders()

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["OrderID", "UserID", "TableNumber", "Status", "Update", "Delete"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def load_orders(self):
        """
        Load orders from the database and display them in the table.
        """
        self.table.setRowCount(0)
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT rs_order_id, rs_user_id, rs_table_number, rs_status FROM orders")
                for row_number, row_data in enumerate(cursor):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data.values()):
                        self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.table.setCellWidget(row_number, 4, self.create_update_button(row_data['rs_order_id']))
                    self.table.setCellWidget(row_number, 5, self.create_delete_button(row_data['rs_order_id']))
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def create_update_button(self, orderID):
        """
        Create an update button for a table row.
        """
        btn_update = QPushButton('Update')
        btn_update.clicked.connect(lambda: self.open_update_order_dialog(orderID))
        return btn_update

    def create_delete_button(self, orderID):
        """
        Create a delete button for a table row.
        """
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.delete_order(orderID))
        return btn_delete

    def delete_order(self, orderID):
        """
        Delete an order from the database.
        """
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            "Are you sure you want to delete this order and all of its details?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("DELETE FROM orderdetails WHERE rs_order_id = %s", (orderID,))
                    cursor.execute("DELETE FROM orders WHERE rs_order_id = %s", (orderID,))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Order and order details deleted successfully.")
                    self.load_orders()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "Order deletion cancelled.")

    def open_update_order_dialog(self, orderID):
        """
        Open the update dialog for an order.
        """
        dialog = UpdateOrderDialog(orderID, self.db_connection, self)
        dialog.exec()
        self.load_orders()


class UpdateOrderDialog(QDialog):
    def __init__(self, orderID, db_connection, parent=None):
        """
        Initialize the UpdateOrderDialog for updating an order.
        """
        super().__init__(parent)
        self.orderID = orderID
        self.db_connection = db_connection
        self.setWindowTitle('Update Order')
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        """
        Set up the dialog's UI elements.
        """
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.table_number_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["placed", "prepared", "served", "paid"])

        form_layout.addRow("TableNumber:", self.table_number_input)
        form_layout.addRow("Status:", self.status_input)

        self.update_button = QPushButton("Update Order")
        self.update_button.clicked.connect(self.update_order)

        layout.addLayout(form_layout)
        layout.addWidget(self.update_button)

        self.load_order_data()

    def load_order_data(self):
        """
        Load existing data for the order into the dialog's fields.
        """
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT rs_table_number, rs_status FROM orders WHERE rs_order_id = %s", (self.orderID,))
                order = cursor.fetchone()
                if order:
                    self.table_number_input.setText(str(order['rs_table_number']))
                    self.status_input.setCurrentText(order['rs_status'])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load order data: {e}")

    def update_order(self):
        """
        Update the order in the database.
        """
        tableNumber = self.table_number_input.text()
        status = self.status_input.currentText()

        if not all([tableNumber, status]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        confirmation = QMessageBox.question(self, "Confirm Update",
                                            "Are you sure you want to update this order?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    orderTime = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
                    cursor.execute("UPDATE orders SET rs_table_number=%s, rs_order_time=%s, rs_status=%s WHERE rs_order_id=%s",
                                   (tableNumber, orderTime, status, self.orderID))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Order updated successfully.")
                    self.accept()  # Close the dialog
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "Order update cancelled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = OrderManagement()
    window.show()
    sys.exit(app.exec())
