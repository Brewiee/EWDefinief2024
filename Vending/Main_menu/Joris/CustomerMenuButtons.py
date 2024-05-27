from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt, Slot
import subprocess

class CustomerDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Dashboard')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Add a stretchable space to center the buttons vertically
        layout.addStretch()

        button1 = QPushButton()
        button1.setIcon(QIcon("customer_lookup.png"))  # Assuming you have customer_lookup.png icon
        button1.setIconSize(QSize(150, 150))
        button1.setFixedSize(200, 200)
        button1.clicked.connect(self.open_customer_lookup)

        button2 = QPushButton()
        button2.setIcon(QIcon("new_customer.png"))  # Assuming you have new_customer.png icon
        button2.setIconSize(QSize(150, 150))
        button2.setFixedSize(200, 200)
        button2.clicked.connect(self.open_new_customer)

        label1 = QLabel("Customer Lookup")
        label1.setAlignment(Qt.AlignCenter)

        label2 = QLabel("New Customer")
        label2.setAlignment(Qt.AlignCenter)

        layout.addWidget(button1)
        layout.addWidget(label1)
        layout.addWidget(button2)
        layout.addWidget(label2)

        # Add another stretchable space to center the buttons horizontally
        layout.addStretch()

    @Slot()
    def open_customer_lookup(self):
        try:
            subprocess.Popen(["python", r"path_to_customer_lookup_script.py"])
        except FileNotFoundError:
            print("Customer lookup script not found or unable to open.")

    @Slot()
    def open_new_customer(self):
        try:
            subprocess.Popen(["python", r"path_to_new_customer_script.py"])
        except FileNotFoundError:
            print("New customer script not found or unable to open.")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = CustomerDashboard()
    window.show()
    sys.exit(app.exec())
