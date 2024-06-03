import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, \
    QSizePolicy, QGridLayout
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices, QFont
from PySide6.QtCore import Qt, QUrl

from Vending.Product_manager.ProductGUI import ProductGUI
from Vending.Stock_manager.inventory_manager_GUI import inventory_manager
from Vending.Report_manager.sales_reports_GUI_v2 import report_manager
from Vending.Vending_machine_manager.Vending_machine_manager_GUI import VendingMachineManagerGUI
from Vending.Log_creator.class_custom_logger import CustomLogger


class LoveWindow(QWidget):
    """
    A class to display the content of a love file in a separate window.
    """

    def __init__(self, content):
        super().__init__()
        self.setWindowTitle('Love')
        self.setGeometry(100, 100, 400, 300)

        # Create a vertical layout for the window
        layout = QVBoxLayout()

        # Create a text edit widget to display the content
        self.text_edit = QTextEdit()
        font = QFont("Courier New")
        font.setPointSize(12)
        self.text_edit.setFont(font)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(content)

        # Add the text edit widget to the layout
        layout.addWidget(self.text_edit)

        # Set the layout to the window
        self.setLayout(layout)


class MainLayout(QWidget):
    """
    The main layout of the application, containing the main menu and navigation buttons.
    """

    def __init__(self):
        super().__init__()

        # Initialize the logger
        self.logger = CustomLogger("Vending", "Logging")
        self.logger.log_debug("Start Main Menu Debug Log")

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface.
        """
        self.setWindowTitle('Main Layout')
        ICON_FOLDER = "../Icons/"
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(100, 100, 1920, 1080)
        self.showMaximized()

        # Create layout for logo and love label
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("newlogo.png")

        # Set the logo if the pixmap is valid
        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_layout.addWidget(self.logo_label, alignment=Qt.AlignRight | Qt.AlignTop)
            self.logo_label.setCursor(Qt.PointingHandCursor)
            self.logo_label.mousePressEvent = self.open_website

        love_label = QLabel("This program was designed with love ❤️")
        love_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        love_label.setCursor(Qt.PointingHandCursor)
        love_label.mousePressEvent = self.open_love_file

        # Create home button
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.show_main_layout)

        # Create layout for buttons
        buttons_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.central_widget)

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(logo_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(love_label)
        main_layout.addWidget(home_button, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.setLayout(main_layout)
        self.show_main_layout()


    def open_website(self, event):
        """
        Open the specified website in the default web browser.
        """
        QDesktopServices.openUrl(QUrl("https://example.com"))

    def open_love_file(self, event):
        """
        Open the love.txt file and display its content in a new window.
        """
        file_path = "love.txt"
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.love_window = LoveWindow(content)
                self.love_window.show()
        except FileNotFoundError:
            print("File not found")

    def show_main_layout(self):
        """
        Show the main layout of the application.
        """
        self.clear_central_layout()
        buttons_dashboard = Dashboard(self)
        self.central_layout.addWidget(buttons_dashboard)
        self.central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttons_dashboard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def clear_central_layout(self):
        """
        Clear all widgets from the central layout.
        """
        while self.central_layout.count():
            item = self.central_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)


class Dashboard(QWidget):
    """
    The dashboard widget that contains buttons for navigating to different parts of the application.
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Initialize the logger
        self.logger = CustomLogger("Vending", "Logging")
        self.logger.log_debug("Start Dashboard Debug Log")

        # Initialize the user interface
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface of the dashboard.
        """
        self.setWindowTitle('Dashboard')
        self.setGeometry(100, 100, 1920, 1080)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QGridLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Configure the buttons and add them to the layout
        self.configure_buttons(main_layout)
        self.setLayout(main_layout)

    def configure_buttons(self, layout):
        """
        Configure the buttons for the dashboard and add them to the layout.
        """
        icons_dir = "../Icons/"
        button_labels = ["Products", "Vending Machines", "Stock Management", "Reports"]

        # Ensure the buttons are displayed in a 2x2 grid
        positions = [(i, j) for i in range(2) for j in range(2)]

        for position, label in zip(positions, button_labels):
            icon_filename = f"{label.lower().replace(' ', '_')}.png"

            button = QPushButton()
            pixmap = QPixmap(icons_dir + icon_filename)
            icon = QIcon(pixmap.scaled(170, 170, Qt.KeepAspectRatio))
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())
            button.setFixedSize(200, 200)

            # Add the button to the layout
            layout.addWidget(button, position[0] * 2, position[1], Qt.AlignCenter)

            method_name = f"open_{label.lower().replace(' ', '_')}"
            button.clicked.connect(getattr(self, method_name))

            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter)

            # Add the label directly below the button
            layout.addWidget(label_widget, position[0] * 2 + 1, position[1], Qt.AlignCenter)

            self.logger.log_debug(f"{label} manager activated")

    def open_products(self):
        """
        Open the product management GUI.
        """
        self.clear_layout()
        self.product_GUI = ProductGUI()
        self.product_GUI.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().addWidget(self.product_GUI)

    def open_vending_machines(self):
        """
        Open the vending machine management GUI.
        """
        self.clear_layout()
        self.vending_machine_manager = VendingMachineManagerGUI()
        self.vending_machine_manager.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().addWidget(self.vending_machine_manager)

    def open_stock_management(self):
        """
        Open the stock management GUI.
        """
        self.clear_layout()
        self.stock_manager = inventory_manager()
        self.stock_manager.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().addWidget(self.stock_manager)

    def open_reports(self):
        """
        Open the reports management GUI.
        """
        self.clear_layout()
        self.reports_manager = report_manager()
        self.reports_manager.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout().addWidget(self.reports_manager)

    def clear_layout(self):
        """
        Clear all widgets from the layout.
        """
        while self.layout().count():
            item = self.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)


if __name__ == '__main__':
    """
    The main entry point of the application.
    """
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    # Create and show the main layout
    main_layout = MainLayout()
    main_layout.show()

    # Start the application's event loop
    sys.exit(app.exec())
