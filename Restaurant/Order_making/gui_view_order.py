import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox,
                               QTreeView)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal
from pymysql import connect, cursors




class ViewOrder(QMainWindow):
    # Define a custom signal for closing
    about_to_close = Signal()

    def __init__(self, db_connection, table_number):
        super().__init__()
        self.db_connection = db_connection
        self.table_number = table_number
        # Assign table_number to an attribute
        self.setWindowTitle("View Order")
        self.setGeometry(100, 100, 400, 300)  # Adjusted for better display of treeview
        self.initUI()
        self.view_order(table_number)

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.setGeometry(100, 100, 1000, 600)

        self.order_view = QTreeView()
        self.order_model = QStandardItemModel()
        self.order_view.setModel(self.order_model)
        self.order_model.setHorizontalHeaderLabels(["Name", "Amount", "Price", "Subtotal"])

        self.order_view.setColumnWidth(0, 350)  # Name column
        self.order_view.setColumnWidth(1, 100)  # Amount column
        self.order_view.setColumnWidth(2, 100)  # Price column
        self.order_view.setColumnWidth(3, 100)  # Subtotal column

        layout.addWidget(self.order_view)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def connect_to_database(self):
        try:
            return connect()
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Unable to connect to the database: {e}")
            return None

    def view_order(self, table_number):
        try:
            with self.db_connection.cursor() as cursor:
                # First, let's get the latest OrderID for the given table number where the table status is 'Occupied'
                cursor.execute("""
                    SELECT o.rs_order_id
                    FROM Orders o
                    JOIN tables t ON o.rs_table_number = t.rs_number
                    WHERE t.rs_number = %s AND t.rs_status = 'Occupied'
                    ORDER BY o.rs_order_time DESC
                    LIMIT 1
                """, (table_number,))
                result = cursor.fetchone()
                print(result)
                if result:
                    latest_order_id = result['rs_order_id']
                    # Now we get the items for that order
                    cursor.execute("""
                        SELECT mi.rs_name, od.rs_quantity, mi.rs_price, (od.rs_quantity * mi.rs_price) AS Subtotal
                        FROM orderdetails od
                        JOIN menu_items mi ON od.rs_item_id = mi.rs_item_id
                        WHERE od.rs_order_id = %s
                    """, (latest_order_id,))
                    data = cursor.fetchall()
                    self.order_model.removeRows(0, self.order_model.rowCount())  # Clear existing rows
                    for item in data:
                        row = [QStandardItem(str(value)) for value in item.values()]
                        self.order_model.appendRow(row)
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred while fetching order details: {e}")

    def closeEvent(self, event):
        # Emit the about_to_close signal when the window is closing
        self.about_to_close.emit()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = ViewOrder()
    main_window.show()
    sys.exit(app.exec())
