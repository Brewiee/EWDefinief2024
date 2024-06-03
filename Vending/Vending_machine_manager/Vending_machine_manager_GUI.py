from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication, QPushButton, QGridLayout,
                               QLabel, QLineEdit, QMessageBox, QComboBox)
from PySide6.QtCore import Qt
import sys
from Vending.Vending_machine_manager.Vending_machine_interface import vending_machine_interface
from Vending.Log_creator.class_custom_logger import CustomLogger
from Vending.Database_connector.class_database_connector import database_connector

class VendingMachineManagerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vending Machine Manager")
        self.setGeometry(100, 100, 800, 600)

        # Initialize logger and vending machine interface
        self.logger = CustomLogger("Vending", "Logging")
        self.vending_machine_interface = vending_machine_interface()

        # Initialize database connection
        db_connector = database_connector()
        self.connection = db_connector.database_connection()

        self.logger.log_info("Start Vending Creator")

        # Initialize GUI components
        self.create_widgets()
        self.combo_signal_connected = False
        self.vending_machine_combo.hide()
        self.product_combo.hide()
        self.machine_set_up_combo.hide()

        # State variables to track ongoing operations
        self.save_in_progress = False
        self.creating_machine = False
        self.vending_machine_change_in_progress = False
        self.delete_operation_in_progress = False

    def create_widgets(self):
        """Create the widgets for the GUI."""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        buttons_layout = QHBoxLayout()
        main_layout.addLayout(buttons_layout)

        # Create buttons with their respective handlers
        button_data = [("Create vending machine", self.create_machine),
                       ("Update vending machine", self.update_machine),
                       ("Delete vending machine", self.delete_machine),
                       ("Set up vending machine", self.set_up_machine),
                       ("Quit", QApplication.instance().quit)]

        for text, handler in button_data:
            button = QPushButton(text)
            button.clicked.connect(handler)
            button.setStyleSheet("text-align:left;")
            buttons_layout.addWidget(button)

        # Combo boxes for vending machines and products
        self.vending_machine_combo = QComboBox()
        main_layout.addWidget(self.vending_machine_combo)
        self.product_combo = QComboBox()
        main_layout.addWidget(self.product_combo)
        self.machine_set_up_combo = QComboBox()
        main_layout.addWidget(self.machine_set_up_combo)

        # Layout for input fields
        input_layout = QGridLayout()
        main_layout.addLayout(input_layout)
        input_layout.setColumnStretch(1, 1)
        main_layout.addStretch(1)

        # Input fields for vending machine details
        self.location_label = QLabel("Vending machine location:")
        input_layout.addWidget(self.location_label, 0, 0)
        self.location_entry = QLineEdit()
        self.location_entry.setPlaceholderText("Enter vending machine location")
        input_layout.addWidget(self.location_entry, 0, 1)

        self.address_label = QLabel("Vending machine address:")
        input_layout.addWidget(self.address_label, 1, 0)
        self.address_entry = QLineEdit()
        self.address_entry.setPlaceholderText("Enter vending machine address")
        input_layout.addWidget(self.address_entry, 1, 1)

        self.postal_label = QLabel("Vending machine postal code:")
        input_layout.addWidget(self.postal_label, 2, 0)
        self.postal_entry = QLineEdit()
        self.postal_entry.setPlaceholderText("Enter vending machine postal code")
        input_layout.addWidget(self.postal_entry, 2, 1)

        self.city_label = QLabel("Vending machine city:")
        input_layout.addWidget(self.city_label, 3, 0)
        self.city_entry = QLineEdit()
        self.city_entry.setPlaceholderText("Enter vending machine city")
        input_layout.addWidget(self.city_entry, 3, 1)

        self.country_label = QLabel("Vending machine country:")
        input_layout.addWidget(self.country_label, 4, 0)
        self.country_entry = QLineEdit()
        self.country_entry.setPlaceholderText("Enter vending machine country")
        input_layout.addWidget(self.country_entry, 4, 1)

        # Buttons for saving, adding products, and confirming deletion
        self.save_button = QPushButton("Save")
        input_layout.addWidget(self.save_button, 5, 0, 1, 2)
        self.save_button.clicked.connect(self.save_vending_machine)
        self.save_button.hide()

        self.add_button = QPushButton("Add")
        input_layout.addWidget(self.add_button, 6, 0, 1, 2)
        self.add_button.clicked.connect(self.add_product_to_inventory)
        self.add_button.hide()

        self.confirm_delete_button = QPushButton("Delete")
        input_layout.addWidget(self.confirm_delete_button, 7, 0, 1, 2)
        self.confirm_delete_button.clicked.connect(self.confirm_delete)
        self.confirm_delete_button.hide()

    def save_vending_machine(self):
        """Save the vending machine details to the database."""
        self.save_button.setEnabled(False)

        if self.save_in_progress:
            return

        self.save_in_progress = True

        # Retrieve input data
        vending_location = self.location_entry.text()
        vending_address = self.address_entry.text()
        vending_postal_str = self.postal_entry.text()
        vending_city = self.city_entry.text()
        vending_country = self.country_entry.text()

        # Validate postal code
        if vending_postal_str.strip() == "":
            QMessageBox.warning(self, "Error", "Postal code cannot be empty!")
            self.reset_save_button()
            return

        try:
            vending_postal = int(vending_postal_str)
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid postal code!")
            self.reset_save_button()
            return

        # Create or update vending machine based on the current state
        if self.creating_machine:
            self.vending_machine_interface.create_vending_machine(vending_location, vending_address, vending_postal,
                                                                  vending_city, vending_country)
            QMessageBox.information(self, "Success", "Vending machine created successfully!")
        else:
            selected_machine_id = self.vending_machine_combo.currentData()
            success = self.vending_machine_interface.update_vending_machine(selected_machine_id, vending_location,
                                                                            vending_address, vending_postal,
                                                                            vending_city, vending_country)
            if success:
                QMessageBox.information(self, "Success", "Vending machine updated successfully!")
                self.populate_vending_machine_menu()
            else:
                QMessageBox.warning(self, "Error", "Failed to update vending machine!")

        self.save_in_progress = False
        self.save_button.setEnabled(True)

    def reset_save_button(self):
        """Reset the state of the save button."""
        self.save_in_progress = False
        self.save_button.setEnabled(True)

    def create_machine(self):
        """Prepare the interface for creating a new vending machine."""
        self.creating_machine = True
        self.clear_input_fields()
        self.add_button.hide()
        self.save_button.show()
        self.vending_machine_combo.hide()
        self.confirm_delete_button.hide()
        self.product_combo.hide()
        self.machine_set_up_combo.hide()

        if self.combo_signal_connected:
            self.vending_machine_combo.currentIndexChanged.disconnect(self.handle_vending_machine_change)
            self.combo_signal_connected = False

    def populate_vending_machine_menu(self):
        """Populate the vending machine drop-down menu."""
        self.vending_machine_combo.clear()
        self.vending_machine_combo.addItem("Please select a vending machine")

        vending_machines = self.vending_machine_interface.choose_vending_machine()
        if vending_machines:
            for machine_id, machine_location in vending_machines:
                self.vending_machine_combo.addItem(machine_location, machine_id)
        else:
            QMessageBox.warning(self, "Warning", "No vending machines found.")

    def populate_product_combo(self):
        """Populate the product drop-down menu."""
        self.product_combo.clear()
        self.product_combo.addItem("Please select a product")

        products = self.vending_machine_interface.read_products()
        if products:
            for product_id, product in products:
                self.product_combo.addItem(product, product_id)
        else:
            QMessageBox.warning(self, "Warning", "No products found.")

    def handle_vending_machine_change(self, index):
        """Handle changes in the vending machine selection."""
        if self.vending_machine_change_in_progress:
            return

        self.vending_machine_change_in_progress = True

        selected_machine_id = self.vending_machine_combo.itemData(index, Qt.UserRole)
        if selected_machine_id is not None and index != 0:
            selected_machine = self.vending_machine_combo.currentText()
            machine_data = self.vending_machine_interface.get_vending_machine_data(selected_machine)
            if machine_data:
                self.fill_input_fields(machine_data)
            else:
                QMessageBox.warning(self, "Warning", "Failed to retrieve vending machine data.")

        self.vending_machine_change_in_progress = False

    def fill_input_fields(self, machine_data):
        """Fill the input fields with data from the given machine_data dictionary."""
        self.location_entry.setText(machine_data.get('vd_vending_machine_location', ''))
        self.address_entry.setText(machine_data.get('vd_vending_machine_address', ''))
        self.postal_entry.setText(machine_data.get('vd_vending_machine_postal_code', ''))
        self.city_entry.setText(machine_data.get('vd_vending_machine_city', ''))
        self.country_entry.setText(machine_data.get('vd_vending_machine_country', ''))

    def clear_input_fields(self):
        """Clear the text in all input fields."""
        self.location_entry.clear()
        self.address_entry.clear()
        self.postal_entry.clear()
        self.city_entry.clear()
        self.country_entry.clear()

    def update_machine(self):
        """Prepare the interface for updating an existing vending machine."""
        self.clear_input_fields()
        self.creating_machine = False
        self.save_button.show()
        self.product_combo.hide()
        self.confirm_delete_button.hide()
        self.machine_set_up_combo.hide()
        self.populate_vending_machine_menu()
        self.vending_machine_combo.show()

        if not self.combo_signal_connected:
            self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)
            self.combo_signal_connected = True
        else:
            self.vending_machine_combo.currentIndexChanged.disconnect(self.handle_vending_machine_change)
            self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)

    def delete_machine(self):
        """Prepare the interface for deleting a vending machine."""
        self.creating_machine = False
        self.clear_input_fields()
        self.product_combo.hide()
        self.save_button.hide()
        self.add_button.hide()
        self.machine_set_up_combo.hide()
        self.populate_vending_machine_menu()
        self.vending_machine_combo.show()
        self.confirm_delete_button.show()

        if not self.combo_signal_connected:
            self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)
            self.combo_signal_connected = True

        self.vending_machine_combo.currentIndexChanged.disconnect(self.handle_vending_machine_change)
        self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)

    def confirm_delete(self):
        """Confirm deletion of the selected vending machine."""
        selected_index = self.vending_machine_combo.currentIndex()
        selected_machine = self.vending_machine_combo.currentText()
        selected_machine_id = self.vending_machine_combo.itemData(selected_index, Qt.UserRole)

        if selected_index > 0 and selected_machine_id:
            self.perform_delete_operation(selected_machine_id, selected_machine)
        else:
            QMessageBox.warning(self, "Warning", "Please select a vending machine to delete.")

    def perform_delete_operation(self, selected_machine_id, selected_machine):
        """Perform the deletion of the selected vending machine."""
        if selected_machine_id is not None:
            confirm_dialog = QMessageBox.question(self, "Confirm Deletion",
                                                  f"Are you sure you want to delete vending machine '{selected_machine}'?",
                                                  QMessageBox.Yes | QMessageBox.No)
            if confirm_dialog == QMessageBox.Yes:
                success = self.vending_machine_interface.delete_vending_machine(selected_machine_id)
                if success:
                    self.logger.log_info(f"Vending machine id: {selected_machine_id} deleted successfully!")
                    QMessageBox.information(self, "Success", "Vending machine deleted successfully!")
                    self.populate_vending_machine_menu()
                    self.clear_input_fields()
                else:
                    self.logger.log_info(f"Failed to delete vending machine id {selected_machine_id}!")
        else:
            self.logger.log_error("No vending machine selected")

    def set_up_machine(self):
        """Set up products in the vending machine."""
        self.creating_machine = False
        self.confirm_delete_button.hide()
        self.save_button.hide()
        self.vending_machine_combo.show()
        self.populate_vending_machine_menu()
        self.product_combo.show()
        self.populate_product_combo()
        self.add_button.show()
        self.clear_input_fields()

        if not self.combo_signal_connected:
            self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)
            self.combo_signal_connected = True

        self.vending_machine_combo.currentIndexChanged.disconnect(self.handle_vending_machine_change)
        self.vending_machine_combo.currentIndexChanged.connect(self.handle_vending_machine_change)

    def add_product_to_inventory(self):
        """Add a product to the vending machine inventory."""
        selected_index = self.vending_machine_combo.currentIndex()
        selected_machine = self.vending_machine_combo.currentText()
        selected_machine_id = self.vending_machine_combo.itemData(selected_index, Qt.UserRole)
        selected_product_index = self.product_combo.currentIndex()
        selected_product = self.product_combo.currentText()
        selected_product_id = self.product_combo.itemData(selected_product_index, Qt.UserRole)

        self.logger.log_info(f"Selected index: {selected_index}, Selected machine: {selected_machine},"
                             f"Selected machine ID: {selected_machine_id}, Selected product index: {selected_product_index}"
                             f"Selected product: {selected_product}, Selected product ID: {selected_product_id} ")

        if selected_machine_id is None:
            QMessageBox.warning(self, "Error", "Please select a vending machine.")
            return

        if selected_product_id is None:
            QMessageBox.warning(self, "Error", "Please select a product.")
            return

        success = self.vending_machine_interface.set_up_vending_machine(selected_machine_id, selected_product_id)

        if success:
            QMessageBox.information(self, "Success", "Product added to vending machine inventory!")
        else:
            QMessageBox.warning(self, "Error", "Failed to add product to vending machine inventory!")

def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VendingMachineManagerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
