import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget
from PySide6.QtCore import QTimer
import pymysql.cursors
from gui_choice_menu import MainMenu

USER = 7


def connect_to_database():
    try:
        db_host = 'localhost'
        db_user = 'dbadmin'
        db_password = 'dbadmin'
        db_name = 'restaurantv2'
        db_connection = pymysql.connect(host=db_host,
                                         user=db_user,
                                         password=db_password,
                                         database=db_name,
                                         cursorclass=pymysql.cursors.DictCursor)
        return db_connection
    except pymysql.MySQLError as e:
        print("Error connecting to the database:", e)
        return None

class TableSelectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user = USER

        self.db_connection = connect_to_database()
        if self.db_connection is None:
            sys.exit("Failed to connect to the database.")


        # self.timer = QTimer()
        # self.timer.timeout.connect(self.load_table_buttons)
        # self.timer.start(300)

        self.init_ui()





    def init_ui(self):
        self.setWindowTitle("Table Selection")
        self.setFixedSize(800, 800)  # Fixed window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Grid layout for buttons
        self.layout = QGridLayout(self.central_widget)
        self.load_table_buttons()

    def load_table_buttons(self):
        try:
            with self.db_connection.cursor() as cursor:
                # Fetch table records
                sql = "SELECT * FROM `tables`"
                cursor.execute(sql)
                tables = cursor.fetchall()

                # Clear existing buttons
                for i in reversed(range(self.layout.count())):
                    widget = self.layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

                # Calculate button size
                num_cols = 4  # Number of columns in the grid
                num_rows = len(tables) // num_cols + (len(tables) % num_cols > 0)
                button_width = self.width() // num_cols
                button_height = self.height() // num_rows

                # Create a button for each table record
                for i, table in enumerate(tables):
                    table_number = table['Number']  # Get the 'Number' from the table record
                    status = table['Status']
                    # print(f"Table {table_number} with status {status}")
                    button = QPushButton(f"{table_number}")  # Set the button text using 'Number'
                    # Make the font of the button bigger and bold
                    font = button.font()
                    font.setPointSize(20)
                    font.setBold(True)
                    button.setFont(font)
                    button.setFixedSize(100, 100)

                    # Set button color based on status
                    color = 'green' if status == 'available' else 'red' if status == 'occupied' else 'blue' if status == 'locked' else 'yellow'
                    button.setStyleSheet(f"background-color: {color}; color: black;")

                    # Connect the button to the create_click_handler method
                    button.clicked.connect(self.create_click_handler_wrapper(table_number, status))
                    self.layout.addWidget(button, i // num_cols, i % num_cols)
        except pymysql.MySQLError as e:
            print("Error loading table buttons:", e)

    def create_click_handler_wrapper(self, table_number, status):
        """Wrapper function to create a callable function for button click without lambda"""
        return lambda: self.create_click_handler(table_number, status)

    def create_click_handler(self, table_number, status):
        """Handle button click"""
        # print(f"Table {table_number} selected with status {status}")
        self.option_choice(table_number, status)

    def option_choice(self, table_number, status):
        print(f"this is gui_table user:{self.user}")
        # self.hide()
        self.choice_menu = MainMenu(db_connection=self.db_connection, table_number=table_number, status=status, user1 = self.user)
        self.choice_menu.about_to_close.connect(self.refresh_table_status)
        # Connect the about_to_close signal of choice_menu to refresh_table_status
        self.choice_menu.about_to_close.connect(self.choice_menu.close)
        self.choice_menu.show()


    def refresh_table_status(self):
        # Refresh the table buttons
        self.load_table_buttons()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = TableSelectionWindow()
    window.show()
    sys.exit(app.exec())
