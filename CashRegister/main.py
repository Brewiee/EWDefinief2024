from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QAction, QPainter, QPixmap, QColor, QPalette, Qt, QIcon
import sys
import os
from CustomerInterface import CustomerManagementApp
from SupplierInterface import SupplierManagementApp
from ProductInterface import ProductManagementApp
from InvoiceInterface import InvoiceManagementApp
from InventoryInterface import InventoryManagementApp
from StBackOrderInterface import StBackOrderManagementApp
from SaBackOrderInterface import SaBackOrderManagementApp

ICON_FOLDER = "../Icons/"

class MainMenuApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 1920, 1080)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setLayout(self.layout)
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

        self.menu_bar = self.menuBar()
        self.customers_menu = self.menu_bar.addMenu("Customers")
        self.suppliers_menu = self.menu_bar.addMenu("Suppliers")
        self.products_menu = self.menu_bar.addMenu("Products")
        self.invoices_menu = self.menu_bar.addMenu("Invoices")
        self.close_menu = self.menu_bar.addMenu("CLOSE")

        self.add_menu_action(self.customers_menu, "Manage Customers", self.open_customer_management)
        self.add_menu_action(self.suppliers_menu, "Manage Suppliers", self.open_supplier_management)
        self.add_menu_action(self.products_menu, "Manage Products", self.open_product_management)
        self.add_menu_action(self.products_menu, "Manage Inventory", self.open_inventory_management)
        self.add_menu_action(self.products_menu, "Manage Storage Backorder", self.open_stbackorder_management)
        self.add_menu_action(self.products_menu, "Manage Sales Backorder", self.open_sabackorder_management)
        self.add_menu_action(self.invoices_menu, "Manage Invoices", self.open_invoice_management)
        self.add_menu_action(self.close_menu, "Close Current Window", self.close_current_window)
        self.add_menu_action(self.close_menu, "Close Application", self.close_application)

        self.current_widget = None

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap_path = os.path.join(ICON_FOLDER, "horse.png")
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
        self.open_management_window(CustomerManagementApp, "Manage Customers")

    @Slot()
    def open_product_management(self):
        self.open_management_window(ProductManagementApp, "Manage Products")

    @Slot()
    def open_inventory_management(self):
        self.open_management_window(InventoryManagementApp, "Manage Inventory")

    @Slot()
    def open_stbackorder_management(self):
        self.open_management_window(StBackOrderManagementApp, "Manage Storage Backorder")

    @Slot()
    def open_sabackorder_management(self):
        self.open_management_window(SaBackOrderManagementApp, "Manage Sales Backorder")

    @Slot()
    def open_supplier_management(self):
        self.open_management_window(SupplierManagementApp, "Manage Suppliers")

    @Slot()
    def open_invoice_management(self):
        self.open_management_window(InvoiceManagementApp, "Manage Invoices")

    def open_management_window(self, management_app_class, window_title):
        if self.current_widget is not None:
            QMessageBox.information(self, 'Warning', 'Close the current window!')
        else:
            self.setWindowTitle(window_title)
            self.current_widget = management_app_class()
            self.layout.addWidget(self.current_widget)

    @Slot()
    def close_current_window(self):
        if self.current_widget is not None:
            reply = QMessageBox.question(self, "Close Window",
                                         "Data that has not been saved will be lost. Do you want to close the current window?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.layout.removeWidget(self.current_widget)
                self.current_widget.deleteLater()
                self.current_widget = None
                self.setWindowTitle("Main Menu")

    @Slot()
    def close_application(self):
        reply = QMessageBox.question(self, "Close Application", "Do you want to close?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Close Application", "Do you want to close?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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