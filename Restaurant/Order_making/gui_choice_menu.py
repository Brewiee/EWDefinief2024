import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QMessageBox
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon
from gui_create_order import CreateOrder
from gui_view_order import ViewOrder
from gui_close_order import ViewOrderToClose
from gui_update_order import UpdateOrder
from gui_lock_table import LockTheTable, UnlockTheTable

ICON_FOLDER = "../../Icons/"

class MainMenu(QMainWindow):
    # Define a custom signal
    about_to_close = Signal()

    def __init__(self, db_connection, table_number, status, user1):
        """
        Initialize the main menu window with database connection and table details.
        """
        super().__init__()
        self.db_connection = db_connection
        self.table_number = table_number
        self.user = user1
        self.status = status
        self.setWindowTitle("Restaurant Management System")
        self.setGeometry(100, 100, 300, 200)

        # Initialize the UI elements
        self.initUI()

    def initUI(self):
        """
        Set up the main window's UI elements.
        """
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Create and configure buttons
        self.create_order_button = self.create_button("Create Order", 100, 50)
        self.close_order_button = self.create_button("Close Order", 100, 50)
        self.update_order_button = self.create_button("Update Order", 100, 50)
        self.view_order_button = self.create_button("View Order", 100, 50)
        self.lock_table_button = self.create_button("Lock", 100, 100, bold=True)
        self.unlock_table_button = self.create_button("Unlock", 100, 100, bold=True)

        # Disable all buttons initially
        self.disable_all_buttons()

        # Enable buttons based on table status
        self.update_button_states()

        # Connect button signals to their respective slots
        self.create_order_button.clicked.connect(self.create_order)
        self.close_order_button.clicked.connect(self.close_order)
        self.update_order_button.clicked.connect(self.update_order)
        self.view_order_button.clicked.connect(self.view_order)
        self.lock_table_button.clicked.connect(self.lock_table)
        self.unlock_table_button.clicked.connect(self.unlock_table)

        # Add buttons to the layout
        layout.addWidget(self.create_order_button)
        layout.addWidget(self.close_order_button)
        layout.addWidget(self.update_order_button)
        layout.addWidget(self.view_order_button)
        layout.addSpacing(20)
        layout.addWidget(self.lock_table_button)
        layout.addSpacing(20)
        layout.addWidget(self.unlock_table_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Set window icon
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def create_button(self, text, width, height, bold=False):
        """
        Helper function to create a QPushButton with specified properties.
        """
        button = QPushButton(text)
        button.setFixedSize(width, height)
        if bold:
            button.setStyleSheet("font-weight: bold;")
        return button

    def disable_all_buttons(self):
        """
        Disable all buttons.
        """
        self.create_order_button.setEnabled(False)
        self.close_order_button.setEnabled(False)
        self.update_order_button.setEnabled(False)
        self.view_order_button.setEnabled(False)
        self.lock_table_button.setEnabled(False)
        self.unlock_table_button.setEnabled(False)

    def update_button_states(self):
        """
        Enable or disable buttons based on the table status.
        """
        if self.status == 'available':
            self.lock_table_button.setEnabled(True)
            self.lock_table_button.setStyleSheet("background-color: green;")
        elif self.status == 'occupied':
            self.enable_buttons([self.close_order_button, self.update_order_button, self.view_order_button])
        elif self.status == 'reserved':
            self.create_order_button.setEnabled(True)
            self.create_order_button.setStyleSheet("background-color: green;")
        elif self.status == 'locked':
            self.enable_buttons([self.create_order_button, self.unlock_table_button])

    def enable_buttons(self, buttons):
        """
        Enable a list of buttons and set their background color to green.
        """
        for button in buttons:
            button.setEnabled(True)
            button.setStyleSheet("background-color: green;")

    def create_order(self):
        """
        Handle the create order button click event.
        """
        self.order_creation = CreateOrder(connection=self.db_connection, table_number=self.table_number, status=self.status, user=self.user)
        self.order_creation.about_to_close.connect(self.close_menu)
        self.order_creation.show()
        self.about_to_close.emit()

    def close_order(self):
        """
        Handle the close order button click event.
        """
        self.order_closing = ViewOrderToClose(connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.order_closing.about_to_close.connect(self.close_menu)
        self.order_closing.show()
        self.about_to_close.emit()

    def update_order(self):
        """
        Handle the update order button click event.
        """
        self.order_updating = UpdateOrder(connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.order_updating.show()
        self.about_to_close.emit()

    def view_order(self):
        """
        Handle the view order button click event.
        """
        self.order_viewing = ViewOrder(db_connection=self.db_connection, table_number=self.table_number)
        self.order_viewing.about_to_close.connect(self.close_menu)
        self.order_viewing.show()

    def close_menu(self):
        """
        Emit the about_to_close signal and close the main menu window.
        """
        self.about_to_close.emit()
        self.close()

    def lock_table(self):
        """
        Handle the lock table button click event.
        """
        self.table_locking = LockTheTable(db_connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.table_locking.about_to_close.connect(self.close_menu)
        self.about_to_close.emit()
        self.close()

    def unlock_table(self):
        """
        Handle the unlock table button click event.
        """
        self.table_locking = UnlockTheTable(db_connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.table_locking.about_to_close.connect(self.close_menu)
        self.about_to_close.emit()
        self.close()

def main():
    """
    Entry point for the application.
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main_window = MainMenu(None, None, None, None)  # Placeholder values
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
