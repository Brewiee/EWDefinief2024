import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QMessageBox,
                               QTreeView)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Signal
from pymysql import connect, cursors

ICON_FOLDER = "../Icons/"

class ViewOrder(QMainWindow):
    # Define a custom signal for closing
    about_to_close = Signal()

    def __init__(self, db_connection, table_number):
        """
        Initialize the ViewOrder window with the given database connection and table number.
        """
        super().__init__()
        self.db_connection = db_connection
        self.table_number = table_number
        self.setWindowTitle("View Order")
        self.setGeometry(100, 100, 400, 300)  # Adjusted for better display of treeview
        self.initUI()
        self.view_order()

    def initUI(self):
        """
        Set up the main window's UI elements.
        """
        widget = QWidget()
        layout = QVBoxLayout()

        self.order_view = QTreeView()
        self.order_model = QStandardItemModel()
        self.order_view.setModel(self.order_model)
        self.order_model.setHorizontalHeaderLabels(["Name", "Amount", "Price", "Subtotal"])

        # Set column widths
        self.order_view.setColumnWidth(0, 350)  # Name column
        self.order_view.setColumnWidth(1, 100)  # Amount column
        self.order_view.setColumnWidth(2, 100)  # Price column
        self.order_view.setColumnWidth(3, 100)  # Subtotal column

        layout.addWidget(self.order_view)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Set window icon
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def view_order(self):
        """
        Fetch and display the current order details for the table.
        """
        try:
            with self.db_connection.cursor() as cursor:
                # Get the latest OrderID for the given table number where the table status is 'Occupied'
                cursor.execute("""
                    SELECT o.rs_order_id
                    FROM orders o
                    JOIN tables t ON o.rs_table_number = t.rs_number
                    WHERE t.rs_number = %s AND t.rs_status = 'occupied'
                    ORDER BY o.rs_order_time DESC
                    LIMIT 1
                """, (self.table_number,))
                result = cursor.fetchone()
                if result:
                    latest_order_id = result['rs_order_id']
                    # Get the items for that order
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
                else:
                    QMessageBox.information(self, "No Orders", "No orders found for the selected table.")
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred while fetching order details: {e}")

    def closeEvent(self, event):
        """
        Emit the about_to_close signal when the window is closing.
        """
        self.about_to_close.emit()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    db_connection = connect(host='localhost', user='root', password='', db='restaurant', cursorclass=cursors.DictCursor)
    table_number = 1  # Example table number
    main_window = ViewOrder(db_connection=db_connection, table_number=table_number)
    main_window.show()
    sys.exit(app.exec())
