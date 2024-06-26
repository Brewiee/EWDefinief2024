import sys
import os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
                               QCalendarWidget, QComboBox, QMessageBox)
from PySide6.QtCore import Signal, QDate
import pymysql

ICON_FOLDER = "../Icons/"

class CustomerWindow(QMainWindow):
    # Define a signal for when the window is closing
    closing = Signal()

    def __init__(self):
        """
        Initialize the CustomerWindow for making reservations.
        """
        super().__init__()
        self.setWindowTitle("Customer Reservation")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        """
        Set up the main window's UI elements.
        """
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Create input fields and widgets
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.calendar = QCalendarWidget()
        self.time_combobox = QComboBox()
        self.time_combobox.addItems(
            ["17:00", "17:15", "17:30", "17:45", "18:00", "18:15", "18:30", "18:45", "19:00", "19:15", "19:30",
             "19:45", "20:00", "20:15", "20:30", "20:45", "21:00", "21:15", "21:30", "21:45", "22:00", "22:15",
             "22:30", "22:45", "23:00"])
        self.make_reservation_button = QPushButton("Make Reservation")
        self.make_reservation_button.clicked.connect(self.make_reservation)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_application)

        # Add widgets to the layout
        main_layout.addWidget(QLabel("Name:"))
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(QLabel("Email:"))
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(QLabel("Address:"))
        main_layout.addWidget(self.address_input)
        main_layout.addWidget(QLabel("Phone:"))
        main_layout.addWidget(self.phone_input)
        main_layout.addWidget(QLabel("Amount of People:"))
        main_layout.addWidget(self.amount_input)
        main_layout.addWidget(QLabel("Day:"))
        main_layout.addWidget(self.calendar)
        main_layout.addWidget(QLabel("Time:"))
        main_layout.addWidget(self.time_combobox)
        main_layout.addWidget(self.make_reservation_button)
        main_layout.addWidget(self.exit_button)

        # Set window icon
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def closeEvent(self, event):
        """
        Emit the closing signal when the window is closing.
        """
        self.closing.emit()
        event.accept()

    def make_reservation(self):
        """
        Handle the reservation process, including database insertion and user feedback.
        """
        # Get user input data
        name = self.name_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        amount = self.amount_input.text()
        day = self.calendar.selectedDate().toString("yyyy-MM-dd")
        time = self.time_combobox.currentText()

        # Show confirmation dialog
        confirmation = QMessageBox.question(self, "Confirm Reservation",
                                            "Are you sure you want to make this reservation?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                # Insert customer data into the database
                db = pymysql.connect(host="localhost", user="dbadmin", password="dbadmin", database="restaurant")
                cursor = db.cursor()
                cursor.execute("INSERT INTO customer (rs_name, rs_email, rs_address, rs_phone_number) VALUES (%s, %s, %s, %s)",
                               (name, email, address, phone))
                db.commit()

                # Get the generated customer ID
                cursor.execute("SELECT LAST_INSERT_ID()")
                customer_id = cursor.fetchone()[0]

                # Insert reservation data into the database
                cursor.execute(
                    "INSERT INTO reservation (rs_customer_id, rs_reservation_date, rs_reservation_time, rs_party_size) VALUES (%s, %s, %s, %s)",
                    (customer_id, day, time, amount))
                db.commit()
                db.close()

                # Clear all input fields
                self.name_input.clear()
                self.email_input.clear()
                self.address_input.clear()
                self.phone_input.clear()
                self.amount_input.clear()
                self.calendar.setSelectedDate(QDate.currentDate())
                self.time_combobox.setCurrentIndex(0)

                # Show success message
                QMessageBox.information(self, "Reservation Confirmation", "Reservation made successfully!")
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred while making the reservation: {e}")

    def exit_application(self):
        """
        Close the application.
        """
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    customer_window = CustomerWindow()
    customer_window.closing.connect(app.quit)  # Connect the closing signal to the application's quit slot

    customer_window.show()
    sys.exit(app.exec())
