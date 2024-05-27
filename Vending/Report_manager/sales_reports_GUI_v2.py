from Vending.Report_manager.class_sales_reports import sales_report_manager
from PySide6.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QLabel,
                               QDateEdit, QMessageBox, QTableWidgetItem, QTableWidget, QPushButton, QHeaderView,
                               QSizePolicy)

from PySide6.QtCore import Qt, QDate
import sys
from Vending.Report_manager.sales_graph_widget import SalesGraphWidget
from Vending.PDF_creator.class_create_PDF import create_pdf
import time
from Vending.Log_creator.class_custom_logger import CustomLogger

class report_manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Report Manager")
        self.setGeometry(100, 100, 800, 600)
        self.logger = CustomLogger("Sales_Report_GUI", "Logging")
        self.logger.log_info("Sales Report GUI Info Log")

        self.sales_report_manager = sales_report_manager()

        self.create_widgets()

        self.populate_vending_machine_menu()

        # Initialize the sales graph widget
        self.sales_graph_widget = SalesGraphWidget(self)
        self.layout.addWidget(self.sales_graph_widget)
        self.sales_graph_widget.hide()  # Hide the sales graph widget initiall
    def create_widgets(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Create a vertical layout
        self.layout = QVBoxLayout()  # Define self.layout
        main_widget.setLayout(self.layout)

        # Create a dropdown menu
        self.combo_box = QComboBox()
        self.combo_box.addItem("Please choose the report here")
        self.combo_box.addItem("Sales report")
        self.combo_box.addItem("Sales graph")
        self.combo_box.addItem("Top three products")
        self.combo_box.addItem("Top three machines")
        self.combo_box.addItem("VAT report")
        self.combo_box.addItem("Payment method report")
        self.layout.addWidget(self.combo_box)

        # Create vending machine drop-down menu
        self.vending_machine_combo = QComboBox()
        self.layout.addWidget(self.vending_machine_combo)

        # Add a horizontal layout for date selection
        date_layout = QHBoxLayout()
        self.layout.addLayout(date_layout)

        # Create "From" date label and date edit widget
        from_label = QLabel("From:")
        self.from_date_edit = QDateEdit()
        self.from_date_edit.setCalendarPopup(True)
        date_layout.addWidget(from_label)
        date_layout.addWidget(self.from_date_edit)

        # Create "Till" date label and date edit widget
        till_label = QLabel("Till:")
        self.till_date_edit = QDateEdit()
        self.till_date_edit.setCalendarPopup(True)
        date_layout.addWidget(till_label)
        date_layout.addWidget(self.till_date_edit)

        # Add a vertical layout for the "GO" button
        go_layout = QVBoxLayout()
        self.layout.addLayout(go_layout)

        # Add "GO" button
        go_button = QPushButton("GO")
        go_button.clicked.connect(self.generate_report)
        go_layout.addWidget(go_button)

        # add "QUIT" button
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)  # Connect the "Quit" button to close the window
        go_layout.addWidget(quit_button)

        # Add spacer to push the "GO" button to the top
        go_layout.addStretch()

        # Create a layout for displaying the report table (initially hidden)
        self.table_layout = QVBoxLayout()
        self.layout.addLayout(self.table_layout)

        # Add a button for generating PDF reports
        self.pdf_button = QPushButton("Generate PDF")
        self.pdf_button.clicked.connect(self.generate_pdf_report)
        self.layout.addWidget(self.pdf_button)

        # Set the default "from" date to "01-01-2024"
        default_from_date = QDate(2024, 1, 1)
        self.from_date_edit.setDate(default_from_date)

        # Set the default "till" date to the current date
        current_date = QDate.currentDate()
        self.till_date_edit.setDate(current_date)


    def populate_vending_machine_menu(self):
        # Clear any existing items in the combo box
        self.vending_machine_combo.clear()

        # Add the placeholder item first
        self.vending_machine_combo.addItem("Please select a vending machine")

        # Add the "All" option below the placeholder
        self.vending_machine_combo.addItem("All")

        vending_machines = self.sales_report_manager.choose_vending_machine()
        if vending_machines:
            for machine_id, machine_location in vending_machines:
                self.vending_machine_combo.addItem(machine_location, machine_id)
        else:
            QMessageBox.warning(self, "Warning", "No vending machines found.")

    def generate_report(self):
        # Clear the existing table layout
        self.clear_layout(self.table_layout)
        # Get the selected start and end dates
        start_date = self.from_date_edit.date()
        end_date = self.till_date_edit.date()

        # Convert the dates to string format
        start_date_str = start_date.toString(Qt.ISODate)
        end_date_str = end_date.toString(Qt.ISODate)

        # Get the selected report type
        report_type = self.combo_box.currentText()

        # Get the selected vending machine ID
        if self.vending_machine_combo.currentText() == "All":
            vending_machine_id = None  # Set vending_machine_id to None for "All" option
        else:
            # Get the vending machine ID from the combo box
            vending_machine_id = self.vending_machine_combo.currentData()

        # Perform actions based on the selected report type and vending machine
        if report_type == "Sales report":
            if vending_machine_id is None:
                # Call a method to generate the overall sales report using the selected dates
                self.display_overall_sales_report(start_date_str, end_date_str)
                self.logger.log_info("Overall sales report All Machines created")
            else:
                # Call a method to generate the sales report for the selected vending machine using the selected dates
                self.display_sales_report(start_date_str, end_date_str, vending_machine_id)
                self.logger.log_info(f"Overall sales report vending machine id {vending_machine_id} created")
        elif report_type == "Sales graph":
            if vending_machine_id is None:
                # Call a method to generate the overall sales report using the selected dates
                self.display_overall_sales_graph(start_date_str, end_date_str)
                self.logger.log_info("Sales graph All Machines created")
            else:
                # Call a method to generate the sales report for the selected vending machine using the selected dates
                self.display_sales_graph(start_date_str, end_date_str, vending_machine_id)
                self.logger.log_info(f"Sales graph vending machine id {vending_machine_id} created")
        elif report_type == "Top three products":
            # Call the method to generate top products report
            self.display_top_three_products(start_date_str, end_date_str)
            self.logger.log_info("Top three products report created")
        elif report_type == "Top three machines":
            # Call the method to generate top machines report
            self.display_top_three_vending_machines(start_date_str, end_date_str)
            self.logger.log_info("Top three vending machines report created")
        elif report_type == "VAT report":
            # Call the method to generate VAT report
            self.display_vat_report(start_date_str, end_date_str)
            self.logger.log_info("VAT report created")
        elif report_type == "Payment method report":
            # Call the method to generate payment method report
            self.display_payment_method_report(start_date_str, end_date_str)
            self.logger.log_info("Payment method report created")
        else:
            # Handle the case when no valid option is selected
            pass

    def display_report_table(self, report_data):
        # This method will display the report table below the "GO" button
        # Clear any existing widgets in the table layout
        for i in reversed(range(self.table_layout.count())):
            self.table_layout.itemAt(i).widget().setParent(None)

        if report_data:
            # Create the table widget and populate it with the report data
            report_table = QTableWidget()
            # Populate the table...
            # Add the table widget to the table layout
            self.table_layout.addWidget(report_table)
        else:
            QMessageBox.warning(self, "Warning", "Failed to generate report.")
            self.logger.log_error("Failed to generate report")

    def display_overall_sales_report(self, start_date, end_date):
        # Call the overall sales report method from the sales report manager
        sales_data = self.sales_report_manager.overall_sales_report(start_date, end_date)
        if sales_data:
            # Sort the data based on the total price column
            sales_data.sort(key=lambda x: float(x[2]), reverse=True)  # Sort based on the third element (total_price)

            # Move the "total" row to the last position
            total_row = [row for row in sales_data if row[0] == 'total']
            if total_row:
                sales_data.remove(total_row[0])
                sales_data.append(total_row[0])

            # Create a QTableWidget to display sales data
            sales_table = QTableWidget()
            sales_table.setColumnCount(4)
            sales_table.setHorizontalHeaderLabels(["Product Name", "Total Sold", "Total Price", "Total VAT"])

            # Populate the table with sorted sales data
            for row, (product_name, total_sold, total_price, total_vat) in enumerate(sales_data):
                sales_table.insertRow(row)
                sales_table.setItem(row, 0, QTableWidgetItem(product_name))
                sales_table.setItem(row, 1, NumericTableWidgetItem(total_sold))
                sales_table.setItem(row, 2, NumericTableWidgetItem(total_price))
                sales_table.setItem(row, 3, NumericTableWidgetItem(total_vat))

            # Enable sorting by clicking the headers
            sales_table.setSortingEnabled(True)

            # Stretch columns to fit the available width
            sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Set the size policy for the table
            sales_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Adjust the size of the table
            sales_table.setMinimumSize(600, 460)  # Adjust these values according to your preference

            # Add the table to the existing layout
            self.table_layout.addWidget(sales_table)

        else:
            QMessageBox.warning(self, "Warning", "Failed to retrieve overall sales report.")
            self.logger.log_error("Failed to retrieve overall sales report.")

    def display_sales_report(self, start_date, end_date, vending_machine_id):
        sales_data = self.sales_report_manager.sales_report(vending_machine_id, start_date, end_date)
        if sales_data:
            # Sort the data based on the total price column
            sales_data.sort(key=lambda x: float(x[2]), reverse=True)  # Sort based on the third element (total_price)

            # Move the "total" row to the last position
            total_row = [row for row in sales_data if row[0] == 'total']
            if total_row:
                sales_data.remove(total_row[0])
                sales_data.append(total_row[0])

            # Create a QTableWidget to display sales data
            sales_table = QTableWidget()
            sales_table.setColumnCount(4)
            sales_table.setHorizontalHeaderLabels(["Product Name", "Total Sold", "Total Price", "Total VAT"])

            # Populate the table with sorted sales data
            for row, (product_name, total_sold, total_price, total_vat) in enumerate(sales_data):
                sales_table.insertRow(row)
                sales_table.setItem(row, 0, QTableWidgetItem(product_name))
                sales_table.setItem(row, 1, NumericTableWidgetItem(total_sold))
                sales_table.setItem(row, 2, NumericTableWidgetItem(total_price))
                sales_table.setItem(row, 3, NumericTableWidgetItem(total_vat))

            # Enable sorting by clicking the headers
            sales_table.setSortingEnabled(True)

            # Stretch columns to fit the available width
            sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Set the size policy for the table
            sales_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Adjust the size of the table
            sales_table.setMinimumSize(600, 460)  # Adjust these values according to your preference

            # Add the table to the existing layout
            self.table_layout.addWidget(sales_table)

        else:
            QMessageBox.warning(self, "Warning", "Failed to retrieve overall sales report.")
            self.logger.log_error("Failed to retrieve overall sales report.")

    def display_overall_sales_graph(self, start_date, end_date, show_graph=True):
        # Clear only the layout containing the graph widget
        self.hide_sales_graph_widget()

        # Show the sales graph widget
        self.show_sales_graph_widget()

        # Get sales data
        sales_data = self.sales_report_manager.overall_sales_graph(start_date, end_date)

        if show_graph:
            if sales_data:
                # Pass sales data to the graph widget
                self.sales_graph_widget.update_graph(sales_data)
            else:
                # Handle the case when no sales data is available
                pass
        else:
            # Hide the graph if show_graph is False
            self.sales_graph_widget.hide()

        # Add the sales graph widget back to the layout
        self.layout.addWidget(self.sales_graph_widget)

    def display_sales_graph(self, start_date, end_date, vending_machine_id, show_graph=True):
        # Remove any existing graph widget from the layout
        self.hide_sales_graph_widget()

        # Show the sales graph widget
        self.show_sales_graph_widget()

        # Get sales data
        sales_data = self.sales_report_manager.sales_graph(vending_machine_id, start_date, end_date)

        if show_graph:
            if sales_data:
                # Pass sales data to the graph widget
                self.sales_graph_widget.update_graph(sales_data)
            else:
                # Handle the case when no sales data is available
                pass
        else:
            # Hide the graph if show_graph is False
            self.sales_graph_widget.hide()

    def display_top_three_products(self, start_date, end_date):
        # clear table if existing
        self.clear_report_table()
        # Retrieve top three products data from the sales report manager
        top_products_data = self.sales_report_manager.top_three_products(start_date, end_date)

        if top_products_data:
            # Create a QTableWidget to display top three products
            top_products_table = QTableWidget()
            top_products_table.setColumnCount(2)
            top_products_table.setHorizontalHeaderLabels(["Product Name", "Total Sold"])

            # Populate the table with top three products data
            for row, (product_name, total_sold) in enumerate(top_products_data):
                top_products_table.insertRow(row)
                top_products_table.setItem(row, 0, QTableWidgetItem(product_name))
                top_products_table.setItem(row, 1, QTableWidgetItem(str(total_sold)))  # Convert to string

            # Stretch columns to fit the available width
            top_products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Set the size policy for the table
            top_products_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Adjust the size of the table
            top_products_table.setMinimumSize(600, 460)

            # Add the table to the layout
            self.table_layout.addWidget(top_products_table)

        else:
            QMessageBox.warning(self, "Warning", "Failed to retrieve top three products.")
            self.logger.log_error("Failed to retrieve top three products.")

    def display_top_three_vending_machines(self, start_date, end_date):
        # clear table if existing
        self.clear_report_table()

        # Call the top_three_vending_machines method from the sales report manager
        top_vending_machines_data = self.sales_report_manager.top_three_vending_machines(start_date, end_date)

        if top_vending_machines_data:
            # Create a QTableWidget to display top three vending machines
            top_vending_machines_table = QTableWidget()
            top_vending_machines_table.setColumnCount(3)
            top_vending_machines_table.setHorizontalHeaderLabels(["Machine ID", "Location", "Total Sold"])

            # Populate the table with top three vending machines data
            for row, (machine_id, location, total_sold) in enumerate(top_vending_machines_data):
                top_vending_machines_table.insertRow(row)
                top_vending_machines_table.setItem(row, 0, QTableWidgetItem(str(machine_id)))  # Convert to string
                top_vending_machines_table.setItem(row, 1, QTableWidgetItem(location))
                top_vending_machines_table.setItem(row, 2, QTableWidgetItem(str(total_sold)))  # Convert to string

            # Stretch columns to fit the available width
            top_vending_machines_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Set the size policy for the table
            top_vending_machines_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Adjust the size of the table
            top_vending_machines_table.setMinimumSize(600, 460)  # Adjust these values according to your preference

            # Add the table to the layout
            self.table_layout.addWidget(top_vending_machines_table)
        else:
            QMessageBox.warning(self, "Warning", "Failed to retrieve top three vending machines.")
            self.logger.log_error("Failed to retrieve top three vending machines.")

    def display_vat_report(self, start_date, end_date):
        # clear table if existing
        self.clear_report_table()

        # Call the vat_report method from the sales report manager
        vat_report_data = self.sales_report_manager.vat_report(start_date, end_date)

        if vat_report_data:
            # Create a QTableWidget to display the VAT report
            vat_report_table = QTableWidget()
            vat_report_table.setColumnCount(3)
            vat_report_table.setHorizontalHeaderLabels(["Total Sold", "Total Price", "Total VAT"])

            # Populate the table with VAT report data
            for row, (total_sold, total_price, total_vat) in enumerate(vat_report_data):
                vat_report_table.insertRow(row)
                vat_report_table.setItem(row, 0, QTableWidgetItem(str(total_sold)))  # Convert to string
                vat_report_table.setItem(row, 1, QTableWidgetItem(str(total_price)))  # Convert to string
                vat_report_table.setItem(row, 2, QTableWidgetItem(str(total_vat)))  # Convert to string

            # Stretch columns to fit the available width
            vat_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Set the size policy for the table
            vat_report_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Adjust the size of the table
            vat_report_table.setMinimumSize(600, 460)  # Adjust these values according to your preference

            # Add the table to the layout
            self.table_layout.addWidget(vat_report_table)
        else:
            QMessageBox.warning(self, "Warning", "Failed to retrieve VAT report.")
            self.logger.log_error("Failed to retrieve VAT report.")

    def display_payment_method_report(self, start_date, end_date):
        # clear table if existing
        self.clear_report_table()

        # Call the payment_method_report method from the sales report manager
        payment_method_report_data = self.sales_report_manager.payment_method_report(start_date, end_date)

        if payment_method_report_data:
            # Create a QTableWidget to display the payment method report
            payment_method_report_table = QTableWidget()
            payment_method_report_table.setColumnCount(3)
            payment_method_report_table.setHorizontalHeaderLabels(["Payment Method", "Total Sold", "Total Price"])

            # Populate the table with payment method report data
            for row, (payment_method, total_sold, total_price) in enumerate(payment_method_report_data):
                payment_method_report_table.insertRow(row)
                payment_method_report_table.setItem(row, 0, QTableWidgetItem(payment_method))
                payment_method_report_table.setItem(row, 1, QTableWidgetItem(str(total_sold)))  # Convert to string
                payment_method_report_table.setItem(row, 2, QTableWidgetItem(str(total_price)))  # Convert to string

            # Stretch columns to fit the available width
            payment_method_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Set the size policy for the table
            payment_method_report_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            # Adjust the size of the table
            payment_method_report_table.setMinimumSize(600, 460)  # Adjust these values according to your preference

            # Add the table to the layout
            self.table_layout.addWidget(payment_method_report_table)
        else:
            QMessageBox.warning(self, "Warning", "Failed to retrieve payment method report.")
            self.logger.log_error("Failed to retrieve payment method report.")

    def generate_pdf_report(self):
        # Get the selected report type
        report_type = self.combo_box.currentText()

        # Get the selected start and end dates
        start_date = self.from_date_edit.date().toString(Qt.ISODate)
        end_date = self.till_date_edit.date().toString(Qt.ISODate)

        # Get the selected vending machine ID and name
        vending_machine_id = self.vending_machine_combo.currentData()
        vending_machine_name = self.vending_machine_combo.currentText()

        if report_type == "Sales report":
            if vending_machine_id is None:
                # Call a method to generate the overall sales report using the selected dates
                data = self.sales_report_manager.overall_sales_report(start_date, end_date)
                headers = ["Product Name", "Total Sold", "Total Price", "Total VAT"]
                title = f"Overall Sales Report"
            else:
                # Call a method to generate the sales report for the selected vending machine using the selected dates
                data = self.sales_report_manager.sales_report(vending_machine_id, start_date, end_date)
                headers = ["Product Name", "Total Sold", "Total Price", "Total VAT"]
                title = f"Sales Report - {vending_machine_name}"
        elif report_type == "VAT report":
            # Call the method to generate VAT report
            data = self.sales_report_manager.vat_report(start_date, end_date)
            headers = ["Total Sold", "Total Price", "Total VAT"]
            title = f"VAT Report"
            vending_machine_name = "all"  # Set vending machine name to "all" for VAT report
        elif report_type == "Payment method report":
            # Call the method to generate payment method report
            data = self.sales_report_manager.payment_method_report(start_date, end_date)
            headers = ["Payment Method", "Total Sold", "Total Price"]
            title = f"Payment Method Report"
            vending_machine_name = "all"  # Set vending machine name to "all" for payment method report
        else:
            QMessageBox.warning(self, "Warning", "PDF generation is not supported for this report type.")
            return

        if data:
            # Generate unique filename with timestamp and machine name
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            machine_name = vending_machine_name.replace(" ", "_").lower()
            filename = f"{report_type.replace(' ', '_').lower()}_{machine_name}_{timestamp}.pdf"
            pdf_creator = create_pdf(data, headers, filename, title=title)
            pdf_creator.generate_pdf()
            QMessageBox.information(self, "PDF Generated", f"{report_type} PDF report generated successfully.")
        else:
            QMessageBox.warning(self, "Warning", f"No data available for {report_type}.")

    def show_sales_graph_widget(self):
        # Create and show the SalesGraphWidget
        self.sales_graph_widget = SalesGraphWidget(self)
        # Check if the widget already has a layout
        if self.sales_graph_widget.layout() is None:
            # If not, create a new layout
            graph_layout = QVBoxLayout()
            self.sales_graph_widget.setLayout(graph_layout)
        # Add the widget to the main layout
        self.layout.addWidget(self.sales_graph_widget)
        print("Sales Graph Widget Layout:", self.sales_graph_widget.layout())

    def hide_sales_graph_widget(self):
        # Hide the SalesGraphWidget if it exists
        if hasattr(self, 'sales_graph_widget'):
            self.sales_graph_widget.setParent(None)

    def clear_layout(self, layout):
        if layout is not None:
            print("Clearing layout:", layout)
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)  # Use setParent(None) to properly remove the widget from the layout
                    widget.deleteLater()
                else:
                    # Recursively clear layouts if the item is a layout
                    self.clear_layout(item.layout())
        else:
            print("Layout is None, skipping clear operation.")

    def clear_report_table(self):
        # Check if the layout already contains a table widget
        if self.table_layout.count() > 0:
            # Retrieve the existing table widget
            existing_table = self.table_layout.itemAt(0).widget()
            # Remove the existing table widget from the layout
            self.table_layout.removeWidget(existing_table)
            # Delete the existing table widget to clear it from memory
            existing_table.deleteLater()


class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, value):
        super().__init__(str(value))

    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return super().__lt__(other)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = report_manager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()