from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt, Slot
import subprocess

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Dashboard')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Add a stretchable space to center the buttons vertically
        layout.addStretch()

        button1 = QPushButton()
        button1.setIcon(QIcon("admin_icon.png"))  # Replace with your icon path
        button1.setIconSize(QSize(150, 150))
        button1.setFixedSize(200, 200)
        button1.clicked.connect(self.open_admin_tool)

        label1 = QLabel("Admin Tool")
        label1.setAlignment(Qt.AlignCenter)

        layout.addWidget(button1)
        layout.addWidget(label1)

        # Add another stretchable space to center the buttons horizontally
        layout.addStretch()

    @Slot()
    def open_admin_tool(self):
        try:
            subprocess.Popen(["python", r"path_to_admin_tool.py"])
        except FileNotFoundError:
            print("Admin tool script not found or unable to open.")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec())
