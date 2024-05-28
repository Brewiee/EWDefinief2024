from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QPixmap, QColor
from PySide6.QtCore import QSize, Qt, Slot

import subprocess

class InvoiceDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Invoice Dashboard')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Set dark mode background color
        self.setStyleSheet("background-color: #333333; color: white;")

        # Add a stretchable space to center the buttons vertically
        layout.addStretch()

        button1 = QPushButton()
        button1.setIcon(QIcon("invoice1.png"))
        button1.setIconSize(QSize(150, 150))
        button1.setFixedSize(200, 200)
        button1.clicked.connect(self.open_invoice_viewer_1)
        button1.setStyleSheet("background-color: #555555; color: white; border: none;")

        button2 = QPushButton()
        button2.setIcon(QIcon("invoice2.png"))
        button2.setIconSize(QSize(150, 150))
        button2.setFixedSize(200, 200)
        button2.clicked.connect(self.open_invoice_builder_1)
        button2.setStyleSheet("background-color: #555555; color: white; border: none;")

        label1 = QLabel("Invoice Lookup")
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("color: white;")

        label2 = QLabel("New Invoice")
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("color: white;")

        layout.addWidget(button1)
        layout.addWidget(label1)
        layout.addWidget(button2)
        layout.addWidget(label2)

        # Add another stretchable space to center the buttons horizontally
        layout.addStretch()

    @Slot()
    def open_invoice_viewer_1(self):
        try:
            subprocess.Popen(["python", r"C:\Users\Joris\PycharmProjects\Eindwerk2024\Joris\Program\Invoice\InvoiceViewerCR.py"])
        except FileNotFoundError:
            print("InvoiceViewerCR.py not found or unable to open.")

    @Slot()
    def open_invoice_builder_1(self):
        try:
            subprocess.Popen(["python", r"C:\Users\Joris\PycharmProjects\Eindwerk2024\Joris\Program\Invoice\InvoiceBuilderCR.py"])
        except FileNotFoundError:
            print("InvoiceBuilderCR.py not found or unable to open.")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = InvoiceDashboard()
    window.show()
    sys.exit(app.exec())
