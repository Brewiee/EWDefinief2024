from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize, Qt, Slot
import subprocess

class ReportsDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Reports Dashboard')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Add a stretchable space to center the buttons vertically
        layout.addStretch()

        button1 = QPushButton()
        button1.setIcon(QIcon("reports_icon.png"))  # Replace with your icon path
        button1.setIconSize(QSize(150, 150))
        button1.setFixedSize(200, 200)
        button1.clicked.connect(self.open_reports_tool)

        label1 = QLabel("Reports Tool")
        label1.setAlignment(Qt.AlignCenter)

        layout.addWidget(button1)
        layout.addWidget(label1)

        # Add another stretchable space to center the buttons horizontally
        layout.addStretch()

    @Slot()
    def open_reports_tool(self):
        try:
            subprocess.Popen(["python", r"path_to_reports_tool.py"])
        except FileNotFoundError:
            print("Reports tool script not found or unable to open.")

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = ReportsDashboard()
    window.show()
    sys.exit(app.exec())
