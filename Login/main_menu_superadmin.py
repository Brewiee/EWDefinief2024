import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from stylesheet_superadmin import superadminstylesheet
import subprocess


class main_menu_superadmin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Superadmin Main Menu")
        self.setGeometry(100, 100, 400, 300)  # Setting window position and size

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create buttons
        self.user_manager_button = QPushButton("User Manager")
        self.database_manager_button = QPushButton("Database Manager")

        # Add buttons to the layout
        layout.addWidget(self.user_manager_button)
        layout.addWidget(self.database_manager_button)

        # Apply stylesheet
        self.setStyleSheet(superadminstylesheet.central_widget())
        self.user_manager_button.setStyleSheet(superadminstylesheet.pushbutton())
        self.database_manager_button.setStyleSheet(superadminstylesheet.pushbutton())

        # Connect buttons to slots
        self.user_manager_button.clicked.connect(self.launch_user_manager)
        self.database_manager_button.clicked.connect(self.launch_database_manager)

    def launch_user_manager(self):
        subprocess.Popen(["python", "prog_user_manager.py"])

    def launch_database_manager(self):
        subprocess.Popen(["python", "DBManager.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = main_menu_superadmin()
    main_menu.show()
    sys.exit(app.exec())