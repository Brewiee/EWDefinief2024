import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

class main_menu_vending(QMainWindow):  # Inherit from QMainWindow
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Vending Main Menu")
        self.setGeometry(100, 100, 400, 300)  # Setting window position and size

        label = QLabel("Welcome to the Vending Main Menu", self)
        label.move(50, 50)
        label.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_menu = main_menu_vending()
    main_menu.show()
    sys.exit(app.exec())
