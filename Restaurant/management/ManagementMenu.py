import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout)
from PySide6.QtCore import Qt
# from user_management import UserManagement
from menu_management import MenuManagement
from order_management import OrderManagement
from table_management import TableManagementWidget
from Reservation_management import ReservationManagement

ICON_FOLDER = "../Icons/"
class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Restaurant Management Dashboard")
        self.setGeometry(100, 100, 300, 400)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)

        # user_management_button = QPushButton("User Management")
        # user_management_button.setFixedSize(200, 50)
        # user_management_button.clicked.connect(self.open_user_management)
        # layout.addWidget(user_management_button)

        menu_management_button = QPushButton("Menu Management")
        menu_management_button.setFixedSize(200, 50)
        menu_management_button.clicked.connect(self.open_menu_management)
        layout.addWidget(menu_management_button)

        order_management_button = QPushButton("Order Management")
        order_management_button.setFixedSize(200, 50)
        order_management_button.clicked.connect(self.open_order_management)
        layout.addWidget(order_management_button)

        table_management_button = QPushButton("Table Management")
        table_management_button.setFixedSize(200, 50)
        table_management_button.clicked.connect(self.open_table_management)
        layout.addWidget(table_management_button)

        reservation_management_button = QPushButton("Reservation Management")
        reservation_management_button.setFixedSize(200, 50)
        reservation_management_button.clicked.connect(self.open_reservation_management)
        layout.addWidget(reservation_management_button)

        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))
    # def open_user_management(self):
    #     self.user_management_window = UserManagement()  # Assume you have a UserManagement class defined
    #     self.user_management_window.show()

    def open_menu_management(self):
        self.menu_management_window = MenuManagement()  # Assume you have a MenuManagement class defined
        self.menu_management_window.show()

    def open_order_management(self):
        self.order_management_window = OrderManagement()  # Assume you have an OrderManagement class defined
        self.order_management_window.show()

    def open_table_management(self):
        self.table_management_window = TableManagementWidget()  # Assume you have a TableManagement class defined
        self.table_management_window.show()

    def open_reservation_management(self):
        self.reservation_management_window = ReservationManagement()  # Assume you have a CustomerWindow class defined
        self.reservation_management_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec())
