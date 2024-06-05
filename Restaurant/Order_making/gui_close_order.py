import sys
import os
import uuid
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, QMessageBox, QTreeView, QWidget, QLabel)
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Signal
from pymysql import connect, cursors
from fpdf import FPDF
from datetime import datetime

ICON_FOLDER = "../Icons/"
TAX = 0.15

class ViewOrderToClose(QMainWindow):
    # Define a signal to indicate that the window is about to close
    about_to_close = Signal()

    def __init__(self, connection, table_number, status):
        """
        Initialize the window with the given database connection, table number, and status.
        """
        super().__init__()
        self.db_connection = connection
        self.table_number = table_number
        self.status = status
        self.setWindowTitle("View Order")
        self.setGeometry(100, 100, 1000, 600)  # Adjusted for better display of treeview
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

        # Add QLabel widgets to display total amounts
        self.total_before_tax_label = QLabel("Total before tax: $0.00")
        layout.addWidget(self.total_before_tax_label)

        self.total_after_tax_label = QLabel("Total after tax: $0.00")
        layout.addWidget(self.total_after_tax_label)

        # Add a button for closing the order
        self.close_order_button = QPushButton("Close Order")
        self.close_order_button.clicked.connect(self.close_order)
        layout.addWidget(self.close_order_button)

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
                # Get the latest OrderID for the given table number where the table status is 'occupied'
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
                    # Now get the items for that order
                    cursor.execute("""
                        SELECT mi.rs_name, od.rs_quantity, mi.rs_price, (od.rs_quantity * mi.rs_price) AS Subtotal
                        FROM orderdetails od
                        JOIN menu_items mi ON od.rs_item_id = mi.rs_item_id
                        WHERE od.rs_order_id = %s
                    """, (latest_order_id,))
                    data = cursor.fetchall()
                    self.order_model.removeRows(0, self.order_model.rowCount())  # Clear existing rows
                    total_before_tax = 0
                    for item in data:
                        row = [QStandardItem(str(value)) for value in item.values()]
                        self.order_model.appendRow(row)
                        total_before_tax += item['Subtotal']
                    self.total_before_tax_label.setText(f"Total before tax: EUR {float(total_before_tax):.2f}")
                    self.total_after_tax_label.setText(f"Total after tax: EUR {float(total_before_tax) * (1 + TAX):.2f}")
                else:
                    QMessageBox.information(self, "No Orders", "No orders found for the selected table.")
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred while fetching order details: {e}")

    def close_order(self):
        """
        Handle the closing of the order, updating the database and generating a PDF receipt.
        """
        confirmation = QMessageBox.question(self, "Confirm Close Order", "Are you sure you want to close this order?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    # Get the latest order for the table
                    cursor.execute("""
                        SELECT rs_order_id
                        FROM orders
                        WHERE rs_table_number = %s AND rs_status = 'placed'
                        ORDER BY rs_order_time DESC
                        LIMIT 1
                    """, (self.table_number,))
                    latest_order = cursor.fetchone()

                    if latest_order:
                        latest_order_id = latest_order['rs_order_id']

                        # Update table status to 'available' and order status to 'paid'
                        cursor.execute("UPDATE tables SET rs_status = 'available' WHERE rs_number = %s",
                                       (self.table_number,))
                        cursor.execute("UPDATE orders SET rs_status = 'paid' WHERE rs_order_id = %s",
                                       (latest_order_id,))

                        # Commit the changes
                        self.db_connection.commit()

                        # Print order details to PDF
                        self.print_order_to_pdf()

                        # Inform user that the order has been paid
                        QMessageBox.information(self, "Order Paid", "The order has been successfully paid.")

                        # Emit the about_to_close signal just before closing the window
                        self.about_to_close.emit()
                    else:
                        QMessageBox.warning(self, "No Orders", "No orders found for the selected table.")
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred while closing the order: {e}")
                self.db_connection.rollback()
            self.close()

    def print_order_to_pdf(self):
        """
        Generate a PDF receipt for the order.
        """
        try:
            # Get current month name and year
            current_month_year = datetime.now().strftime("%B_%Y")
            current_date = datetime.now().strftime("%d_%m_%Y")
            current_hour_min = datetime.now().strftime("%H_%M")
            # Generate a unique identifier
            unique_id = str(uuid.uuid4().hex)[:8]  # Get the first 8 characters of a UUID
            # Construct the directory name
            directory_name = f"..\\receipts_{current_month_year}"

            # Construct the filename with the unique identifier
            date_directory = os.path.join(directory_name, current_date)
            filename = os.path.join(date_directory, f"Receipt_{self.table_number}_!{current_hour_min}!_{unique_id}.pdf")

            # Create the directories if they don't exist
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)

            if not os.path.exists(date_directory):
                os.makedirs(date_directory)

            # Combine similar items
            combined_items = {}
            for row in range(self.order_model.rowCount()):
                name = self.order_model.item(row, 0).text()
                quantity = int(self.order_model.item(row, 1).text())
                price = float(self.order_model.item(row, 2).text())
                subtotal = float(self.order_model.item(row, 3).text())

                if name in combined_items:
                    combined_items[name]['quantity'] += quantity
                    combined_items[name]['subtotal'] += subtotal
                else:
                    combined_items[name] = {
                        'quantity': quantity,
                        'price': price,
                        'subtotal': subtotal
                    }

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Order Details", ln=True, align="C")
            pdf.cell(200, 10, txt="Table Number: " + str(self.table_number), ln=True, align="L")
            pdf.cell(200, 10, txt="", ln=True)

            total_before_tax = 0
            for name, details in combined_items.items():
                quantity = details['quantity']
                price = details['price']
                subtotal = details['subtotal']
                total_before_tax += subtotal
                pdf.cell(200, 10,
                         txt=f"Name: {name}, Quantity: {quantity}, Price: {price:.2f}, Subtotal: {subtotal:.2f}",
                         ln=True, align="L")

            total_after_tax = total_before_tax * (1 + TAX)
            pdf.cell(200, 10, txt="", ln=True)  # Add an empty line
            pdf.cell(200, 10, txt=f"Total before tax: EUR {total_before_tax:.2f}", ln=True, align="R", border=True)
            pdf.cell(200, 10, txt=f"Tax (21%): EUR {total_before_tax * TAX:.2f}", ln=True, align="R", border=True)
            pdf.cell(200, 10, txt=f"Total after tax: EUR {total_after_tax:.2f}", ln=True, align="R", border=True)

            pdf.output(filename)

            QMessageBox.information(self, "PDF Saved", f"Order details saved to {filename}")
        except Exception as e:
            QMessageBox.warning(self, "PDF Error", f"An error occurred while printing order details to PDF: {e}")

