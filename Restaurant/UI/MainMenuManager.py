import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, \
    QSpacerItem, QSizePolicy
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices, QFontDatabase, QFont
from MainMenuButtonsManager import Dashboard as ButtonsDashboard
from PySide6.QtCore import Qt, QUrl, QFile, QIODevice
import os

ICON_FOLDER = "../Icons/"
class LoveWindow(QWidget):
    def __init__(self, content):
        super().__init__()
        self.setWindowTitle('Love')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        font = QFont("Courier New")  # Use a font that supports ASCII characters well
        font.setPointSize(12)  # Adjust font size as needed
        self.text_edit.setFont(font)
        self.text_edit.setReadOnly(True)
        # Use Unicode characters for the message
        self.text_edit.setPlainText(content)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)


class MainLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Layout')
        self.setWindowIcon(QIcon("favicon.png"))  # Set window icon
        self.setGeometry(100, 100, 1920, 1080)  # Set window size to 1080p
        self.showMaximized()  # Start the program in full screen mode

        # Create layout for logo and love label
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("newlogo.png")
        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_layout.addWidget(self.logo_label, alignment=Qt.AlignRight | Qt.AlignTop)  # Align logo to top right
            self.logo_label.setCursor(Qt.PointingHandCursor)
            self.logo_label.mousePressEvent = self.open_website


        love_label = QLabel("This program was designed with love ❤️")
        love_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        love_label.setCursor(Qt.PointingHandCursor)
        love_label.mousePressEvent = self.open_love_file

        # Create layout for buttons
        buttons_layout = QVBoxLayout()
        self.buttons_dashboard = ButtonsDashboard()
        buttons_layout.addWidget(self.buttons_dashboard)

        # Create home button
        home_button = QPushButton("Home")
        home_button.clicked.connect(self.show_main_layout)

        # Create empty vertical spacer to align love label and home button
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(logo_layout)
        main_layout.addStretch(1)  # Add stretch to push buttons to the center
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch(1)  # Add stretch to push love label to the bottom
        main_layout.addItem(spacer)
        main_layout.addWidget(love_label)
        main_layout.addWidget(home_button, alignment=Qt.AlignBottom | Qt.AlignLeft)

        self.show()
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def open_website(self, event):
        QDesktopServices.openUrl(QUrl("https://example.com"))

    def open_love_file(self, event):
        file_path = "love.txt"
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.love_window = LoveWindow(content)
                self.love_window.show()
        except FileNotFoundError:
            print("File not found")

    def show_main_layout(self):
        self.close()
        main_layout = MainLayout()
        main_layout.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Set the application style to the default style
    main_layout = MainLayout()
    sys.exit(app.exec())
