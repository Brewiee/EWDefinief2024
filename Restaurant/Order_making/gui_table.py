import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon
import pymysql.cursors
from gui_choice_menu import MainMenu

# Constants for user and icon folder path
USER = 1
ICON_FOLDER = "../../Icons/"

def connect_to_database():
    """
    Establish a connection to the database and return the connection object.
    """
    try:
        db_host = 'localhost'
        db_user = 'dbadmin'
        db_password = 'dbadmin'
        db_name = 'restaurant'
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
        """
        Initialize the main window and connect to the database.
        """
        super().__init__()
        self.user = USER

        # Connect to the database
        self.db_connection = connect_to_database()
        if self.db_connection is None:
            sys.exit("Failed to connect to the database.")

        # Initialize the UI
        self.init_ui()

    def init_ui(self):
        """
        Set up the main window's UI elements.
        """
        self.setWindowTitle("Table Selection")
        self.setFixedSize(800, 800)  # Fixed window size

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Grid layout for buttons
        self.layout = QGridLayout(self.central_widget)
        self.load_table_buttons()

        # Set window icon
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def load_table_buttons(self):
        """
        Load table data from the database and create buttons for each table.
        """
        try:
            with self.db_connection.cursor() as cursor:
                # Fetch table records from the database
                sql = "SELECT * FROM `tables`"
                cursor.execute(sql)
                tables = cursor.fetchall()

                # Clear existing buttons in the layout
                for i in reversed(range(self.layout.count())):
                    widget = self.layout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

                # Calculate button size and layout grid dimensions
                num_cols = 4  # Number of columns in the grid
                num_rows = len(tables) // num_cols + (len(tables) % num_cols > 0)
                button_width = self.width() // num_cols
                button_height = self.height() // num_rows

                # Create a button for each table record
                for i, table in enumerate(tables):
                    table_number = table['rs_number']
                    status = table['rs_status']

                    # Create a button with the table number
                    button = QPushButton(f"{table_number}")

                    # Set button font size and boldness
                    font = button.font()
                    font.setPointSize(20)
                    font.setBold(True)
                    button.setFont(font)
                    button.setFixedSize(100, 100)

                    # Set button color based on table status
                    color = self.get_status_color(status)
                    button.setStyleSheet(f"background-color: {color}; color: black;")

                    # Connect the button to the click handler
                    button.clicked.connect(self.create_click_handler_wrapper(table_number, status))
                    self.layout.addWidget(button, i // num_cols, i % num_cols)
        except pymysql.MySQLError as e:
            print("Error loading table buttons:", e)

    def get_status_color(self, status):
        """
        Return the color associated with the table status.
        """
        if status == 'available':
            return 'green'
        elif status == 'occupied':
            return 'red'
        elif status == 'locked':
            return 'blue'
        else:
            return 'yellow'

    def create_click_handler_wrapper(self, table_number, status):
        """
        Wrapper function to create a callable function for button click without lambda.
        """
        return lambda: self.create_click_handler(table_number, status)

    def create_click_handler(self, table_number, status):
        """
        Handle button click events.
        """
        self.option_choice(table_number, status)

    def option_choice(self, table_number, status):
        """
        Display the options menu for the selected table.
        """
        self.choice_menu = MainMenu(db_connection=self.db_connection, table_number=table_number, status=status, user1=self.user)
        self.choice_menu.about_to_close.connect(self.refresh_table_status)
        self.choice_menu.about_to_close.connect(self.choice_menu.close)
        self.choice_menu.show()

    def refresh_table_status(self):
        """
        Refresh the table buttons to reflect the current status.
        """
        self.load_table_buttons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = TableSelectionWindow()
    window.show()
    sys.exit(app.exec())
