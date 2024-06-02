from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QMessageBox, QLineEdit, QFileDialog
from PySide6.QtGui import QColor, QPalette
from PySide6.QtCore import Qt
import sys
import os
from fpdf import FPDF
from datetime import datetime
import pymysql

# Constants
dbuser = "dbadmin"
dbpass = "dbadmin"
database_db = "CashRegister"

class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value):
        super().__init__(str(value))

    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            try:
                return float(self.text()) < float(other.text())
            except ValueError:
                return self.text() < other.text()
        else:
            return QTableWidgetItem.__lt__(self, other)

class StBackOrderManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Storage Backorder Management")
        self.setGeometry(100, 100, 1920, 1080)

        # Initialize database connection
        try:
            self.conn = pymysql.connect(
                host="localhost",
                user=dbuser,
                password=dbpass,
                database=database_db,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.Error as e:
            QMessageBox.critical(self, "Database Connection Error", f"Failed to connect to database: {e}")
            sys.exit(1)

        self.init_ui()
        self.populate_table()

    def init_ui(self):
        self.layout = QVBoxLayout()

        # Add search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")
        self.search_input.setStyleSheet("color: white;")
        self.search_input.textChanged.connect(self.filter_stbackorders)
        self.layout.addWidget(self.search_input)

        # Add table view for products
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Product Name", "Supplier", "Order Date", "Order Quantity", "Status"])
        self.layout.addWidget(self.table)

        # Enable sorting
        self.table.setSortingEnabled(True)

        # Add save button
        self.btn_save_changes = QPushButton("Save Changes")
        self.btn_save_changes.clicked.connect(self.save_changes)
        self.layout.addWidget(self.btn_save_changes)

        # Print Button
        self.btn_print_pdf = QPushButton("Print Storage Backorder List to PDF")
        self.btn_print_pdf.clicked.connect(self.print_stbackorder_to_pdf)
        self.layout.addWidget(self.btn_print_pdf)

        # Set layout for the central widget
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def populate_table(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        st.CR_StBackorder_Backorder_ID,
                        p.CR_Product_Name,
                        s.CR_Supplier_Name,
                        st.CR_StBackorder_Date,
                        st.CR_StBackorder_Order_Quantity,
                        st.CR_StBackorder_Status
                    FROM 
                        Storage_Backorder st
                    INNER JOIN 
                        Product p ON st.CR_StBackorder_Product_ID = p.CR_Product_Product_ID
                    INNER JOIN 
                        Supplier s ON st.CR_StBackorder_Supplier_ID = s.CR_Supplier_Supplier_ID
                """)
                stbackorders = cursor.fetchall()

                self.table.setRowCount(len(stbackorders))
                for row, stbackorder in enumerate(stbackorders):
                    for col, field in enumerate(stbackorder.values()):
                        if col in [0, 3, 4]:  # Numeric fields
                            item = NumericTableWidgetItem(str(field))
                        else:
                            item = QTableWidgetItem(str(field))
                        if col in [0, 1, 2, 3, 4]:
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Read-only
                        self.table.setItem(row, col, item)

                self.table.resizeColumnsToContents()
                self.table.sortByColumn(0, Qt.AscendingOrder)

        except pymysql.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to load products: {e}")

    def save_changes(self):
        try:
            with self.conn.cursor() as cursor:
                for row in range(self.table.rowCount()):
                    backorder_id = self.table.item(row, 0).text()
                    status = self.table.item(row, 5).text()

                    cursor.execute("""
                        UPDATE Storage_Backorder
                        SET 
                            CR_StBackorder_Status = %s
                        WHERE 
                            CR_StBackorder_Backorder_ID = %s
                    """, (status, backorder_id))
            self.conn.commit()
            self.populate_table()
            QMessageBox.information(self, "Success", "Changes saved successfully.")
        except pymysql.Error as e:
            print("Error saving changes:", e)
            QMessageBox.warning(self, "Error", "Failed to save changes. Please check the console for more information.")

    def print_stbackorder_to_pdf(self):
        try:
            class PDF(FPDF):
                def header(self):
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 10, 'StorageBackorder List - Date: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0,
                              'L')
                    self.ln(20)

            pdf = PDF(orientation='P')
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            headers = ["ID", "Product Name", "Supplier", "Order Date", "Order Quantity", "Status"]

            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        st.CR_StBackorder_Backorder_ID,
                        p.CR_Product_Name,
                        s.CR_Supplier_Name,
                        st.CR_StBackorder_Date,
                        st.CR_StBackorder_Order_Quantity,
                        st.CR_StBackorder_Status
                    FROM 
                        Storage_Backorder st
                    INNER JOIN 
                        Product p ON st.CR_StBackorder_Product_ID = p.CR_Product_Product_ID
                    INNER JOIN 
                        Supplier s ON st.CR_StBackorder_Supplier_ID = s.CR_Supplier_Supplier_ID
                """)
                stbackorders = cursor.fetchall()

                search_text = self.search_input.text().strip().lower()
                if search_text:
                    sorted_stbackorders = [stbackorder for stbackorder in stbackorders if
                                       any(search_text in str(field).lower() for field in stbackorder.values())]
                else:
                    sorted_stbackorders = sorted(stbackorders, key=lambda x: x['CR_StBackorder_Backorder_ID'])

                # Calculate the width for each column
                col_widths = [0] * len(headers)
                pdf.set_font("Arial", size=8)
                for i, header in enumerate(headers):
                    col_widths[i] = max(col_widths[i], pdf.get_string_width(header) + 4)

                for stbackorder in sorted_stbackorders:
                    for i, field in enumerate(stbackorder.values()):
                        col_widths[i] = max(col_widths[i], pdf.get_string_width(str(field)) + 4)

                total_width = sum(col_widths)
                if total_width > pdf.w - 2 * pdf.l_margin:
                    scaling_factor = (pdf.w - 2 * pdf.l_margin) / total_width
                    col_widths = [w * scaling_factor for w in col_widths]

                pdf.set_font("Arial", 'B', 8)
                for i, header in enumerate(headers):
                    pdf.cell(col_widths[i], 10, header, border=1)
                pdf.ln()

                pdf.set_font("Arial", size=8)
                for product in sorted_stbackorders:
                    for i, field in enumerate(product.values()):
                        pdf.cell(col_widths[i], 8, str(field), border=1)
                    pdf.ln()

            filename, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF files (*.pdf)")
            if filename:
                if not filename.endswith(".pdf"):
                    filename += ".pdf"
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                pdf_output_path = f"{filename}_{current_time}.pdf"
                pdf.output(pdf_output_path)

                reply = QMessageBox.information(self, "Success",
                                                f"Storage Backorder list saved to {pdf_output_path}. Do you want to open it?",
                                                QMessageBox.Ok | QMessageBox.Cancel)
                if reply == QMessageBox.Ok:
                    if os.name == 'nt':
                        os.startfile(pdf_output_path)
                    elif os.name == 'posix':
                        os.system(f"xdg-open {pdf_output_path}")

        except pymysql.Error as e:
            QMessageBox.critical(self, "Database Error", f"Failed to print inventory: {e}")

    def filter_stbackorders(self):
        search_text = self.search_input.text().strip().lower()

        for row in range(self.table.rowCount()):
            visible = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().strip().lower():
                    visible = True
                    break
            self.table.setRowHidden(row, not visible)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = StBackOrderManagementApp()
    window.showMaximized()
    sys.exit(app.exec())
