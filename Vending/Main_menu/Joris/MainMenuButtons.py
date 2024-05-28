import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from InvoiceMenuButtons import InvoiceDashboard  # Import the InvoiceDashboard class from InvoiceMenuButtons.py
from CustomerMenuButtons import CustomerDashboard  # Import the CustomerDashboard class from CustomerMenuButtons.py
from StockManagementMenuButtons import StockManagementDashboard  # Import the StockDashboard class from StockMenuButtons.py
from ReportsMenuButtons import ReportsDashboard  # Import the ReportsDashboard class from ReportsMenuButtons.py
from UserMenuButtons import UsersDashboard  # Import the UserDashboard class from UserMenuButtons.py
from AdminMenuButtons import AdminDashboard  # Import the AdminDashboard class from AdminMenuButtons.py

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
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
        # Custom labels for buttons
        button_labels = [
            "Invoices",
            "Customers",
            "Stock Management",
            "Reports",
            "Users",
            "Admin"
        ]

        # Calculate number of rows and columns based on number of buttons
        num_buttons = len(button_labels)
        num_columns = 3 if num_buttons >= 9 else 2 if num_buttons >= 6 else 1
        num_rows = (num_buttons + num_columns - 1) // num_columns

        for i, label in enumerate(button_labels):
            row = i // num_columns
            col = i % num_columns

            button = QPushButton()
            pixmap = QPixmap(f"{label.lower()}.png")
            icon = QIcon(pixmap.scaled(170, 170, Qt.KeepAspectRatio))
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())  # Set the icon size explicitly
            button.setFixedSize(200, 200)  # Set fixed size for buttons
            layout.addWidget(button, row*2, col, 1, 1, Qt.AlignCenter)

            # Connect appropriate method to button click event
            if label == "Invoices":
                button.clicked.connect(self.open_invoice)
            elif label == "Customers":
                button.clicked.connect(self.open_customer)
            elif label == "Stock Management":
                button.clicked.connect(self.open_stock_management)
            elif label == "Reports":
                button.clicked.connect(self.open_reports)
            elif label == "Users":
                button.clicked.connect(self.open_users)
            elif label == "Admin":
                button.clicked.connect(self.open_admin)

            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_widget, row*2+1, col, 1, 1, Qt.AlignCenter)

    def open_invoice(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the invoice dashboard
        self.invoice_dashboard = InvoiceDashboard()
        self.layout().addWidget(self.invoice_dashboard)

    def open_customer(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the customer dashboard
        self.customer_dashboard = CustomerDashboard()
        self.layout().addWidget(self.customer_dashboard)

    def open_stock_management(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the stock management dashboard
        self.stock_management_dashboard = StockManagementDashboard()
        self.layout().addWidget(self.stock_management_dashboard)

    def open_reports(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the reports dashboard
        self.reports_dashboard = ReportsDashboard()
        self.layout().addWidget(self.reports_dashboard)

    def open_users(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the users dashboard
        self.users_dashboard = UsersDashboard()
        self.layout().addWidget(self.users_dashboard)

    def open_admin(self):
        # Clear the layout
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the admin dashboard
        self.admin_dashboard = AdminDashboard()
        self.layout().addWidget(self.admin_dashboard)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Set the application style to the default style
    dashboard = Dashboard()
    sys.exit(app.exec())

