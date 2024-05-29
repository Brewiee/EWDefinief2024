from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox
from PySide6.QtGui import QAction, QColor, Qt, QPixmap, QPainter, QPalette
import sys
import os
import subprocess
from CustomerInterface import CustomerManagementApp
from SupplierInterface import SupplierManagementApp
from ProductInterface import ProductManagementApp
from InvoiceInterface import InvoiceManagementApp

windows_base_dir = "C:/Users/M.Akif Haleplioglu/PycharmProjects/Eindwerk_voorbereiding"

class MainMenuApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 1920, 1080)
        self.initUI()

    def initUI(self):
        # Create the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main layout
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.layout)

        # Create a menu bar
        self.menu_bar = self.menuBar()

        # Add main menu categories
        self.customers_menu = self.menu_bar.addMenu("Customers")
        self.suppliers_menu = self.menu_bar.addMenu("Suppliers")
        self.products_menu = self.menu_bar.addMenu("Products")
        self.invoices_menu = self.menu_bar.addMenu("Invoices")
        self.close_menu = self.menu_bar.addMenu("CLOSE")

        # Add actions to the Customers menu
        self.add_menu_action(self.customers_menu, "Manage Customers", self.open_customer_management)

        # Add actions to the Suppliers menu
        self.add_menu_action(self.suppliers_menu, "Manage Suppliers", self.open_supplier_management)

        # Add actions to the Products menu
        self.add_menu_action(self.products_menu, "Manage Products", self.open_product_management)

        # Add actions to the Invoices menu
        self.add_menu_action(self.invoices_menu, "Manage Invoices", self.open_invoice_management)

        self.add_menu_action(self.close_menu, "Close Window", self.close_application)
        self.add_menu_action(self.close_menu, "Close Application", self.close_application)

        self.current_widget = None  # Keep track of the current widget

    def paintEvent(self, event):
        base_dir = windows_base_dir
        painter = QPainter(self)
        pixmap_path = os.path.join(base_dir, "Icons", "hors.png")
        pixmap = QPixmap(pixmap_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.width() // 2, self.height() // 2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            x = (self.width() - scaled_pixmap.width()) // 2
            y = (self.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            overlay = QColor(255, 255, 255, 0)
            painter.fillRect(x, y, scaled_pixmap.width(), scaled_pixmap.height(), overlay)
        super().paintEvent(event)

    def add_menu_action(self, menu, name, callback):
        action = QAction(name, self)
        action.triggered.connect(callback)
        menu.addAction(action)

    @Slot()
    def open_customer_management(self):
        self.open_management_window(CustomerManagementApp)

    @Slot()
    def open_product_management(self):
        self.open_management_window(ProductManagementApp)

    @Slot()
    def open_supplier_management(self):
        self.open_management_window(SupplierManagementApp)

    @Slot()
    def open_invoice_management(self):
        self.open_management_window(InvoiceManagementApp)

    def open_management_window(self, management_app_class):
        if self.current_widget is not None:
            reply = QMessageBox.question(self, "Close Window",
                                         "Data that has not been saved will be lost. Do you want to close the current window?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            self.layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()
        self.current_widget = management_app_class()
        self.layout.addWidget(self.current_widget)

    @Slot()
    def close_application(self):
        reply = QMessageBox.question(self, "Close Window",
                                     "Do you want to close?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

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

    window = MainMenuApp()
    window.showMaximized()
    sys.exit(app.exec())
