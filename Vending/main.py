import sys
from PySide6.QtWidgets import QApplication
from src.Vending_UI.Main_menu.Main_menu_Vending_manager import MainLayout

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    main_layout = MainLayout()
    sys.exit(app.exec())