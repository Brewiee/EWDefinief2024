import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from src.Vending_UI.Product_manager.ProductGUI import ProductGUI
from src.Vending_UI.Stock_manager.inventory_manager_GUI import inventory_manager
from src.Vending_UI.Report_manager.sales_reports_GUI_v2 import report_manager
from src.Vending_UI.Vending_machine_manager.Vending_machine_manager_GUI import vending_machine_manager_GUI
from src.Vending_UI.Log_creator.class_custom_logger import CustomLogger

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = CustomLogger("Main_Menu", "Logging")
        self.logger.log_debug("Start Main Menu Debug Log")
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard')
        self.setWindowIcon(QIcon("favicon.png"))  # Set window icon
        self.setGeometry(100, 100, 1920, 1080)  # Set window size to 1080p

        # Create main layout
        main_layout = QGridLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Configure buttons
        self.configure_buttons(main_layout)

        self.show()

    def configure_buttons(self, layout):
        # Define the directory containing all icons
        icons_dir = "C:/Syntra/EIndwerk/EIndwerk_final/Joeri/Vending_manager/data/Icons/"

        # Custom labels for buttons
        button_labels = [
            "Products" ,
            "Vending Machines",
            "Stock Management",
            "Reports",
            "Users",
            "Admin"
        ]

        # Calculate number of rows and columns based on number of buttons
        num_buttons = len(button_labels)
        num_columns = 3 if num_buttons >= 9 else 2 if num_buttons >= 6 else 1
        num_rows = (num_buttons + num_columns - 1) // num_columns

        for i, label_data in enumerate(button_labels):
            if isinstance(label_data, tuple):
                label, icon_filename = label_data
            else:
                label = label_data
                icon_filename = f"{label.lower().replace(' ', '_')}.png"

            row = i // num_columns
            col = i % num_columns

            button = QPushButton()
            pixmap = QPixmap(icons_dir + icon_filename)
            icon = QIcon(pixmap.scaled(170, 170, Qt.KeepAspectRatio))
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())  # Set the icon size explicitly
            button.setFixedSize(200, 200)  # Set fixed size for buttons
            layout.addWidget(button, row * 2, col, 1, 1, Qt.AlignCenter)

            # Connect appropriate method to button click event
            method_name = f"open_{label.lower().replace(' ', '_')}"
            button.clicked.connect(getattr(self, method_name))

            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_widget, row * 2 + 1, col, 1, 1, Qt.AlignCenter)

            # Connect appropriate method to button click event
            if label == "Products":
                button.clicked.connect(self.open_products)
                self.logger.log_debug("Products manager activated")
            elif label == "Vending Machines":
                button.clicked.connect(self.open_vending_machines)
                self.logger.log_debug("Vending Machines manager activated")
            elif label == "Stock Management":
                button.clicked.connect(self.open_stock_management)
                self.logger.log_debug("Stock manager activated")
            elif label == "Reports":
                button.clicked.connect(self.open_reports)
                self.logger.log_debug("Reports manager activated")
            elif label == "Users":
                button.clicked.connect(self.open_users)
                self.logger.log_debug("Users activated")
            elif label == "Admin":
                button.clicked.connect(self.open_admin)
                self.logger.log_debug("Admin activated")

            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_widget, row * 2 + 1, col, 1, 1, Qt.AlignCenter)

    def open_products(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the Product GUI
        self.product_GUI = ProductGUI()
        self.logger.log_debug("Product manager Created")
        self.layout().addWidget(self.product_GUI)

    def open_vending_machines(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.vending_machine_manager = vending_machine_manager_GUI()  # Instantiate the class
        self.logger.log_debug("Vending machine manager created")
        self.layout().addWidget(self.vending_machine_manager)

    def open_stock_management(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the stock management dashboard
        self.stock_manager = inventory_manager()
        self.logger.log_debug("Stock manager created")
        self.layout().addWidget(self.stock_manager)

    def open_reports(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the reports dashboard
        self.reports_manager = report_manager()
        self.logger.log_debug("report manager created")
        self.layout().addWidget(self.reports_manager)

    def open_users(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def open_admin(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Set the application style to the default style
    dashboard = Dashboard()
    sys.exit(app.exec())