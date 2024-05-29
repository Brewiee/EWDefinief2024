import sys
from Vending.Stock_manager.class_inventory_management import stock_manager
from Vending.Log_creator.class_custom_logger import CustomLogger
from Vending.PDF_creator.class_create_PDF import create_pdf
from PySide6.QtWidgets import QWidget, QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QTreeWidgetItem, \
    QMessageBox, QTreeWidget, QHeaderView, QLabel, QLineEdit, QDialog, QGridLayout, QComboBox, QSizePolicy
from PySide6.QtGui import Qt

class inventory_manager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Manager")
        self.setGeometry(100, 100, 800, 600)
        self.logger = CustomLogger("Vending", "Logging")
        self.logger.log_info("Start inventory GUI Info Log")

        self.stock_manager = stock_manager()

        self.create_widgets()

        self.tree.itemDoubleClicked.connect(self.edit_record)

        self.populate_vending_machine_menu()

        self.vending_machine_combo.currentIndexChanged.connect(self.update_tree_with_selected_machine)



    def create_widgets(self):
        """Create the widgets for the GUI."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Create buttons layout
        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        button_data = [("set stock to refill value", self.set_stock_to_refill_values),
                       ("Set stock to max value", self.set_stock_to_max_values),
                       ("Show refill values", self.show_stock_to_refill_values),
                       ("Show max values", self.show_stock_to_max_values),
                       ("Quit", QApplication.instance().quit)]

        for text, handler in button_data:
            # Create button
            button = QPushButton(text)
            button.clicked.connect(handler)

            # Set button text alignment
            button.setStyleSheet("text-align:left;")

            buttons_layout.addWidget(button)

        # Create vending machine drop-down menu
        self.vending_machine_combo = QComboBox()
        main_layout.addWidget(self.vending_machine_combo)

        # Create TreeWidget
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["ID", "Product Name", "Current Stock", "Refill Stock", "Max Stock", "Min Stock"])  # Adjust header labels
        main_layout.addWidget(self.tree, stretch=1)

        # Set size policy for the tree widget
        self.tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.Stretch)

        header = self.tree.header()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Connect combo box signal
        self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)

    def populate_vending_machine_menu(self):
        # Clear any existing items in the combo box
        self.vending_machine_combo.clear()

        # Add the placeholder item at index 0
        self.vending_machine_combo.addItem("Please select a vending machine")

        vending_machines = self.stock_manager.choose_vending_machine()
        if vending_machines:
            for machine_id, machine_location in vending_machines:
                self.vending_machine_combo.addItem(machine_location, machine_id)
        else:
            QMessageBox.warning(self, "Warning", "No vending machines found.")

    def update_tree_with_selected_machine(self, index):
        selected_machine_id = self.vending_machine_combo.itemData(index, Qt.UserRole)  # Access item data using UserRole
        if selected_machine_id is not None:  # Check if a vending machine is actually selected
            if index != 0:  # Skip data retrieval if the placeholder item is selected
                self.tree.clear()
                machine_data = self.stock_manager.read_inventory(selected_machine_id)
                if machine_data:
                    for data_row in machine_data:
                        item = QTreeWidgetItem([str(item) for item in data_row])
                        self.tree.addTopLevelItem(item)
                else:
                    QMessageBox.warning(self, "Warning", "No data available for the selected vending machine.")
        else:
            # No vending machine is selected, do nothing or show a message
            pass

    def handle_vending_machine_change(self, index):
        selected_machine_id = self.vending_machine_combo.itemData(index)
        if selected_machine_id is None:
            self.clear_tree_view()
        else:
            self.update_tree_with_selected_machine(selected_machine_id)

    def clear_tree_view(self):
        self.tree.clear()

    def read_products(self):
        try:
            # Clear the existing items in the tree
            self.tree.clear()

            # Get the selected vending machine ID from the combo box
            selected_index = self.vending_machine_combo.currentIndex()
            selected_machine_id = self.vending_machine_combo.itemData(selected_index)

            # Retrieve inventory data specific to the selected vending machine
            inventory_data = self.stock_manager.read_inventory(selected_machine_id)

            if inventory_data:
                for data_row in inventory_data:
                    item = QTreeWidgetItem([str(item) for item in data_row])
                    self.tree.addTopLevelItem(item)
            else:
                QMessageBox.warning(self, "Warning", "No inventory data available for the selected vending machine.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def edit_record(self):
        # Get the selected item
        selected_item = self.tree.currentItem()
        if selected_item:
            # Get the inventory ID of the selected item (assuming it's stored in the first column)
            inventory_id = selected_item.text(0)

            # Get the product name of the selected item
            product_name = selected_item.text(1)  # Assuming the product name is in the second column

            # Get the current values for other fields
            current_values = [
                selected_item.text(2),  # Stock Quantity (assuming it's in the third column)
                selected_item.text(3),  # Refill Stock (assuming it's in the fourth column)
                selected_item.text(4),  # Max Stock (assuming it's in the fifth column)
                selected_item.text(5),  # Min Stock (assuming it's in the sixth column)
            ]

            # Open the edit dialog
            dialog = EditDialog(product_name, current_values, self)
            if dialog.exec():
                edited_data = dialog.get_data()
                # Update the database with edited data
                self.stock_manager.update_inventory(inventory_id, edited_data)
                # Refresh the display
                self.refresh_display()
                self.read_products()
        else:
            QMessageBox.warning(self, "Warning", "Please select a record to edit.")

    def refresh_display(self):
        # Clear the QTreeWidget and re-populate it with updated data
        self.tree.clear()
        self.read_products()

    def set_stock_to_refill_values(self):
        # Get the selected vending machine ID from the combo box
        selected_machine_id = self.vending_machine_combo.currentData()
        if selected_machine_id is not None:
            # Call the set_stock_to_refill method with the selected machine ID
            self.stock_manager.set_stock_to_refill(selected_machine_id)
            self.read_products()
        else:
            QMessageBox.warning(self, "Warning", "Please select a vending machine.")

    def set_stock_to_max_values(self):
        # Get the selected vending machine ID from the combo box
        selected_machine_id = self.vending_machine_combo.currentData()
        if selected_machine_id is not None:
            # Call the set_stock_to_refill method with the selected machine ID
            self.stock_manager.set_stock_to_max(selected_machine_id)
            self.read_products()
        else:
            QMessageBox.warning(self, "Warning", "Please select a vending machine.")

    def show_stock_to_refill_values(self):
        selected_machine_id = self.vending_machine_combo.currentData()
        if selected_machine_id is not None:
            # Retrieve the vending machine data
            vending_machine_data = self.stock_manager.choose_vending_machine()

            # Find the location of the selected machine
            machine_location = None
            for machine_id, location in vending_machine_data:
                if machine_id == selected_machine_id:
                    machine_location = location
                    break

            if machine_location:
                # Retrieve the stock to refill values from the stock manager
                refill_values = self.stock_manager.show_stock_to_refill(selected_machine_id)

                if refill_values:
                    # Generate PDF report for stock to refill values with machine location as title
                    pdf_filename = f"stock_to_refill_report {machine_location}.pdf"
                    pdf_title = f"Stock to Refill Report for Machine: {machine_location}"
                    pdf_data = [["Inventory ID", "Product Name", "Current Stock", "Needed to refill",
                                 "Refill stock"]] + refill_values
                    pdf_headers = ["Inventory ID", "Product Name", "Stock", "Refill", "Refill Stock"]
                    save_path = "C://Syntra//EIndwerk//EIndwerk_final//Joeri//Vending_manager//data//refill_reports"
                    pdf_generator = create_pdf(pdf_data, pdf_headers, pdf_filename, title=pdf_title, save_path=save_path)
                    pdf_generator.generate_pdf()
                    self.logger.log_info(f"PDF saved at: {save_path}")

                    QMessageBox.information(self, "PDF Generated",
                                            f"PDF report for stock to refill values generated: {pdf_filename}")
                else:
                    QMessageBox.warning(self, "Warning", "No data available for the selected vending machine.")
            else:
                QMessageBox.warning(self, "Warning", "Machine location not found for the selected vending machine.")

    def show_stock_to_max_values(self):
        selected_machine_id = self.vending_machine_combo.currentData()
        if selected_machine_id is not None:
            # Retrieve the vending machine data
            vending_machine_data = self.stock_manager.choose_vending_machine()

            # Find the location of the selected machine
            machine_location = None
            for machine_id, location in vending_machine_data:
                if machine_id == selected_machine_id:
                    machine_location = location
                    break

            if machine_location:
                # Retrieve the max stock values from the stock manager
                max_values = self.stock_manager.show_stock_to_max(selected_machine_id)

                if max_values:

                    # Generate PDF report for max stock values
                    pdf_filename = "max_stock_report.pdf"
                    pdf_title = f"stock to max refill report for Machine: {machine_location}"
                    pdf_data = [["Inventory ID", "Product Name", "Current Stock", "Needed to refill", "Max Stock"]] + max_values
                    pdf_headers = ["Inventory ID", "Product Name", "Stock", "Refill", "Max Stock"]
                    save_path = "C://Syntra//EIndwerk//EIndwerk_final//Joeri//Vending_manager//data//refill_reports"
                    pdf_generator = create_pdf(pdf_data, pdf_headers, pdf_filename, title=pdf_title,
                                               save_path=save_path)
                    pdf_generator.generate_pdf()
                    self.logger.log_info(f"PDF saved at: {save_path}")

                    QMessageBox.information(self, "PDF Generated", f"PDF report for max stock values generated: {pdf_filename}")
                else:
                    QMessageBox.warning(self, "Warning", "No data available for the selected vending machine.")
            else:
                QMessageBox.warning(self, "Warning", "Machine location not found for the selected vending machine.")

    def save_changes(self):
        # Retrieve the selected item from the tree
        selected_item = self.tree.currentItem()
        if selected_item:
            # Extract the data from the selected item
            inventory_id = int(selected_item.text(0))  # Assuming ID is in the first column
            new_stock_quantity = int(selected_item.text(2))  # Assuming stock quantity is in the third column
            new_min_stock = int(selected_item.text(3))  # Assuming min stock is in the fourth column
            new_max_stock = int(selected_item.text(4))  # Assuming max stock is in the fifth column
            new_refill_stock = int(selected_item.text(5))  # Assuming refill stock is in the sixth column

            # Update the database with the new values
            success = self.stock_manager.update_inventory(inventory_id, new_stock_quantity, new_min_stock,
                                                          new_max_stock, new_refill_stock)
            if success:
                QMessageBox.information(self, "Success", "Changes saved successfully.")
            else:
                QMessageBox.warning(self, "Error", "Failed to save changes.")

class EditDialog(QDialog):
    def __init__(self, product_name, current_values, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Record")
        layout = QGridLayout(self)

        # Display product name as a label
        product_label = QLabel("Product Name:")
        layout.addWidget(product_label, 0, 0)
        product_value_label = QLabel(product_name)
        layout.addWidget(product_value_label, 0, 1)

        # Create line edits for other data fields
        labels = ["Stock Quantity", "Refill Stock", "Max Stock", "Min Stock"]
        self.line_edits = []
        for row, (label_text, value) in enumerate(zip(labels, current_values), start=1):
            label = QLabel(label_text)
            layout.addWidget(label, row, 0)

            line_edit = QLineEdit(str(value))
            layout.addWidget(line_edit, row, 1)
            self.line_edits.append(line_edit)

        # Create buttons for saving or canceling edits
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        layout.addWidget(save_button, len(labels) + 1, 0, 1, 2)

    def accept(self):
        # Show a message box after clicking save
        QMessageBox.information(self, "Success", "Changes saved successfully.")
        super().accept()  # Call the accept method of the parent QDialog to close the dialog

    def get_data(self):
        # Return edited data from line edits
        return [line_edit.text() for line_edit in self.line_edits]

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = inventory_manager()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()