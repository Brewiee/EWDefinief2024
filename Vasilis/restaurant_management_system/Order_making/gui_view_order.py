import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox,
                               QTreeView)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal
from pymysql import connect, cursors


db_config = {
    'host': 'localhost',
    'user': 'dbadmin',
    'password': 'dbadmin',
    'db': 'restaurantV2',
    'charset': 'utf8mb4',
    'cursorclass': cursors.DictCursor
}

class ViewOrder(QMainWindow):
    # Define a custom signal for closing
    about_to_close = Signal()

    def __init__(self, db_connection, table_number):
        super().__init__()
        self.db_connection = self.connect_to_database()
        self.table_number = table_number
        # Assign table_number to an attribute
        self.setWindowTitle("View Order")
        self.setGeometry(100, 100, 400, 300)  # Adjusted for better display of treeview
        self.initUI()
        self.view_order(table_number)

    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.order_view = QTreeView()
        self.order_model = QStandardItemModel()
        self.order_view.setModel(self.order_model)
        self.order_model.setHorizontalHeaderLabels(["Name", "Amount", "Price", "Subtotal"])

        layout.addWidget(self.order_view)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def connect_to_database(self):
        try:
            return connect(**db_config)
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"Unable to connect to the database: {e}")
            return None

    def view_order(self, table_number):
        try:
            with self.db_connection.cursor() as cursor:
                # First, let's get the latest OrderID for the given table number where the table status is 'Occupied'
                cursor.execute("""
                    SELECT o.OrderID
                    FROM Orders o
                    JOIN tables t ON o.TableNumber = t.Number
                    WHERE t.Number = %s AND t.Status = 'Occupied'
                    ORDER BY o.OrderTime DESC
                    LIMIT 1
                """, (table_number,))
                result = cursor.fetchone()
                print(result)
                if result:
                    latest_order_id = result['OrderID']
                    # Now we get the items for that order
                    cursor.execute("""
                        SELECT mi.Name, od.Quantity, mi.Price, (od.Quantity * mi.Price) AS Subtotal
                        FROM OrderDetails od
                        JOIN MenuItems mi ON od.ItemID = mi.ItemID
                        WHERE od.OrderID = %s
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
