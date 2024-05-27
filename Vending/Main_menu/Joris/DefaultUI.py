import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QIcon, QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dashboard')
        self.setWindowIcon(QIcon("favicon.png"))  # Set window icon
        self.setGeometry(100, 100, 1920, 1080)  # Set window size to 1080p

        # Create layout for logo and love label
        logo_layout = QHBoxLayout()
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("newlogo.png")
        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.logo_label.mousePressEvent = self.open_website  # Connect mousePressEvent to open_website function
            logo_layout.addWidget(self.logo_label, alignment=Qt.AlignRight | Qt.AlignTop)  # Align logo to top right

        love_label = QLabel("This program was designed with love ❤️")
        love_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        love_label.mousePressEvent = self.open_text_file  # Connect mousePressEvent to open_text_file function

        # Create main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(logo_layout)
        main_layout.addWidget(love_label)

        self.show()

    def open_website(self, event):
        QDesktopServices.openUrl(QUrl("https://www.example.com"))

    def open_text_file(self, event):
        print("Opening text file...")  # Print statement to check if the function is being called
        try:
            with open('love.txt', 'r', encoding='utf-8') as file:
                text = file.read()
                self.text_window = TextWindow(text)
                self.text_window.show()
        except Exception as e:
            print("Error:", e)

class TextWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle("Love Text")
        self.setWindowIcon(QIcon("favicon.png"))  # Set window icon
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)  # Align text to center
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")  # Set the application style to the default style
    dashboard = Dashboard()
    sys.exit(app.exec())
