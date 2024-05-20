import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QMessageBox
from PySide6.QtCore import Signal, Qt
from gui_create_order import CreateOrder
from gui_view_order import ViewOrder
from gui_close_order import ViewOrderToClose
from gui_update_order import UpdateOrder
from gui_lock_table import LockTheTable, UnlockTheTable
class MainMenu(QMainWindow):
    # Define a custom signal
    about_to_close = Signal()

    def __init__(self, db_connection, table_number, status, user1):
        super().__init__()
        self.db_connection = db_connection
        self.setWindowTitle("Restaurant Management System")
        self.setGeometry(100, 100, 300, 200)
        self.table_number = table_number
        self.user = user1
        self.status = status
        self.initUI()


        self
    def initUI(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.create_order_button = QPushButton("Create Order")
        self.create_order_button.setFixedSize(100, 50)
        self.close_order_button = QPushButton("Close Order")
        self.close_order_button.setFixedSize(100, 50)
        self.update_order_button = QPushButton("Update Order")
        self.update_order_button.setFixedSize(100, 50)
        self.view_order_button = QPushButton("View Order")
        self.view_order_button.setFixedSize(100, 50)

        self.lock_table_button = QPushButton("Lock") #***************************
        self.lock_table_button.setFixedSize(100, 100)
        self.lock_table_button.setStyleSheet(" font-color: Black; font-weight: bold;")

        self.unlock_table_button = QPushButton("Unlock")  # ***************************
        self.unlock_table_button.setFixedSize(100, 100)
        self.unlock_table_button.setStyleSheet(" font-color: Black; font-weight: bold;")



        # Put all the buttons in disable mode
        self.create_order_button.setEnabled(False)
        self.close_order_button.setEnabled(False)
        self.update_order_button.setEnabled(False)
        self.view_order_button.setEnabled(False)
        self.lock_table_button.setEnabled(False)
        self.unlock_table_button.setEnabled(False)


        # Check status to enable/disable buttons
        if self.status == 'available':
            self.lock_table_button.setEnabled(True)
            self.lock_table_button.setStyleSheet("background-color: green;")

        elif self.status == 'occupied':
            self.close_order_button.setEnabled(True)
            self.close_order_button.setStyleSheet("background-color: green;")
            self.update_order_button.setEnabled(True)
            self.update_order_button.setStyleSheet("background-color: green;")
            self.view_order_button.setEnabled(True)
            self.view_order_button.setStyleSheet("background-color: green;")

        elif self.status == 'reserved':
            self.create_order_button.setEnabled(True)
            self.create_order_button.setStyleSheet("background-color: green;")

        elif self.status == 'locked':
            self.create_order_button.setEnabled(True)
            self.unlock_table_button.setEnabled(True)
            self.create_order_button.setStyleSheet("background-color: green;")
            self.unlock_table_button.setStyleSheet("background-color: green;")

        self.create_order_button.clicked.connect(self.create_order)
        self.close_order_button.clicked.connect(self.close_order)
        self.update_order_button.clicked.connect(self.update_order)
        self.view_order_button.clicked.connect(self.view_order)
        self.lock_table_button.clicked.connect(self.lock_table)
        self.unlock_table_button.clicked.connect(self.unlock_table)

        layout.addWidget(self.create_order_button)
        layout.addWidget(self.close_order_button)
        layout.addWidget(self.update_order_button)
        layout.addWidget(self.view_order_button)
        layout.addSpacing(20)
        layout.addWidget(self.lock_table_button)
        layout.addSpacing(20)
        layout.addWidget(self.unlock_table_button)

        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def create_order(self):
        print(f"this is create order user{self.user}")
        self.order_creation = CreateOrder(connection=self.db_connection, table_number=self.table_number, status=self.status, user = self.user)
        self.order_creation.about_to_close.connect(self.close_menu)
        self.order_creation.show()
        self.about_to_close.emit()


    def close_order(self):
        self.order_closing = ViewOrderToClose(connection=self.db_connection, table_number=self.table_number, status=self.status)
        # Connect the about_to_close signal to the close_menu method
        self.order_closing.about_to_close.connect(self.close_menu)
        self.order_closing.show()
        self.about_to_close.emit()


    def update_order(self):
        self.order_updating = UpdateOrder(connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.order_updating.show()
        self.about_to_close.emit()


    def view_order(self):
        self.order_closing = ViewOrder(db_connection=self.db_connection, table_number=self.table_number)
        self.order_closing.about_to_close.connect(self.close_menu)
        self.order_closing.show()


    def close_menu(self):
        # Emit the about_to_close signal before closing the window
        self.about_to_close.emit()
        # Close the MainMenu window
        self.close()

    def lock_table(self):
        self.table_locking = LockTheTable(db_connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.table_locking.about_to_close.connect(self.close_menu)
        self.about_to_close.emit()
        self.close()




    def unlock_table(self):
        self.table_locking = UnlockTheTable(db_connection=self.db_connection, table_number=self.table_number, status=self.status)
        self.table_locking.about_to_close.connect(self.close_menu)
        self.about_to_close.emit()
        self.close()




def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
