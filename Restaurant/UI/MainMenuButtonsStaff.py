import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
import subprocess
import os

ICON_FOLDER = "../Icons/"

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard')
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))
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
            "Live Ordering System"
        ]

        # Calculate number of rows and columns based on number of buttons
        num_buttons = len(button_labels)
        num_columns = 3 if num_buttons >= 9 else 2 if num_buttons >= 6 else 1
        num_rows = (num_buttons + num_columns - 1) // num_columns

        for i, label in enumerate(button_labels):
            row = i // num_columns
            col = i % num_columns

            button = QPushButton()
            icon_path = os.path.join(ICON_FOLDER, f"{label.lower()}.png")
            pixmap = QPixmap(icon_path)
            icon = QIcon(pixmap.scaled(170, 170, Qt.KeepAspectRatio))
            button.setIcon(icon)
            button.setIconSize(pixmap.rect().size())  # Set the icon size explicitly
            button.setFixedSize(200, 200)  # Set fixed size for buttons
            layout.addWidget(button, row*2, col, 1, 1, Qt.AlignCenter)

            # Connect appropriate method to button click event

            button.clicked.connect(self.open_los)

            label_widget = QLabel(label)
            label_widget.setAlignment(Qt.AlignCenter)
            layout.addWidget(label_widget, row*2+1, col, 1, 1, Qt.AlignCenter)

    def open_los(self):
        try:
            # Get the absolute path to the script
            script_path = os.path.abspath("../Restaurant/Order_making/gui_table.py")
            # Run the script using subprocess.Popen
            subprocess.Popen(["python", script_path])

        except FileNotFoundError:
            print("Unable to find gui_table.py.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Set the application style to the default style
    dashboard = Dashboard()
    sys.exit(app.exec())

