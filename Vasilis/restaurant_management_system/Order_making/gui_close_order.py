import sys
import os
import uuid

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QMessageBox, QTreeView, QWidget, QLabel
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, Signal
from pymysql import connect, cursors
from fpdf import FPDF
from datetime import datetime

TAX = 0.15


class ViewOrderToClose(QMainWindow):
    # Define a signal to indicate that the window is about to close
    about_to_close = Signal()

    def __init__(self, connection, table_number, status):
        super().__init__()
        self.db_connection = connection
        self.table_number = table_number
        self.status = status
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
                    total_before_tax = 0
                    for item in data:
                        row = [QStandardItem(str(value)) for value in item.values()]
                        self.order_model.appendRow(row)
                        total_before_tax += item['Subtotal']
                    self.total_before_tax_label.setText(f"Total before tax: ${total_before_tax:.2f}")
                    self.total_after_tax_label.setText(f"Total after tax: ${float(total_before_tax) * (1 + TAX):.2f}")
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred while fetching order details: {e}")

    def close_order(self):
        confirmation = QMessageBox.question(self, "Confirm Close Order", "Are you sure you want to close this order?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    # Get the latest reservation for the table
                    cursor.execute("""
                        SELECT reservation_id
                        FROM reservation
                        WHERE TableID = %s AND status = 'pending'
                        ORDER BY reservation_date DESC, reservation_time DESC
                        LIMIT 1
                    """, (self.table_number,))
                    reservation = cursor.fetchone()

                    # Update the status of the reservation to 'done' if it exists
                    if reservation:
                        cursor.execute("""
                            UPDATE reservation
                            SET status = 'done'
                            WHERE reservation_id = %s
                        """, (reservation['reservation_id'],))

                    # Update table status to 'available' and order status to 'Paid'
                    cursor.execute("UPDATE tables SET Status = 'available' WHERE Number = %s", (self.table_number,))
                    cursor.execute("UPDATE Orders SET Status = 'Paid' WHERE TableNumber = %s", (self.table_number,))

                    # Commit the changes
                    self.db_connection.commit()

                    # Print order details to PDF
                    self.print_order_to_pdf()

                    # Inform user that the order has been paid
                    QMessageBox.information(self, "Order Paid", "The order has been successfully paid.")

                    # Emit the about_to_close signal just before closing the window
                    self.about_to_close.emit()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred while closing the order: {e}")
                self.db_connection.rollback()
            self.close()


    def print_order_to_pdf(self):
        try:
            # Get current day name and date
            today = datetime.now().strftime("%A_%Y%m%d")
            # Generate a unique identifier
            unique_id = str(uuid.uuid4().hex)[:8]  # Get the first 8 characters of a UUID
            # Construct the directory name
            directory_name = f"receipts_{today}"
            # Construct the filename with the unique identifier
            filename = f"{directory_name}/Receipt_{today}_{self.table_number}_{unique_id}.pdf"

            # Create the directory if it doesn't exist
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Order Details", ln=True, align="C")
            pdf.cell(200, 10, txt="Table Number: " + str(self.table_number), ln=True, align="L")
            pdf.cell(200, 10, txt="", ln=True)
            for row in range(self.order_model.rowCount()):
                name = self.order_model.item(row, 0).text()
                quantity = self.order_model.item(row, 1).text()
                price = self.order_model.item(row, 2).text()
                subtotal = self.order_model.item(row, 3).text()
                pdf.cell(200, 10, txt=f"Name: {name}, Quantity: {quantity}, Price: {price}, Subtotal: {subtotal}",
                         ln=True, align="L")
            pdf.output(filename)

            QMessageBox.information(self, "PDF Saved", f"Order details saved to {filename}")
        except Exception as e:
            QMessageBox.warning(self, "PDF Error", f"An error occurred while printing order details to PDF: {e}")


