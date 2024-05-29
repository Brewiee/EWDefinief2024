from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
                               QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QComboBox, QCalendarWidget)
from PySide6.QtCore import QTimer, Signal
from pymysql import connect, cursors
from datetime import datetime
from Make_Reservations import CustomerWindow

class UpdateReservationDialog(QDialog):
    dialogClosed = Signal()

    def __init__(self, reservation_data, db_connection, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Reservation")
        self.db_connection = db_connection
        self.layout = QVBoxLayout()

        self.customer_name_edit = QLineEdit()
        self.reservation_date_calendar = QCalendarWidget()
        self.reservation_time_combo = QComboBox()
        self.party_size_edit = QLineEdit()
        self.table_number_combo = QComboBox()
        self.reservation_id = None

        self.update_reservation_button = QPushButton("Update Reservation")
        self.update_reservation_button.clicked.connect(self.confirm_update_reservation)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close_dialog)

        self.layout.addWidget(QLabel("Customer Name:"))
        self.layout.addWidget(self.customer_name_edit)
        self.layout.addWidget(QLabel("Reservation Date:"))
        self.layout.addWidget(self.reservation_date_calendar)
        self.layout.addWidget(QLabel("Reservation Time:"))
        self.layout.addWidget(self.reservation_time_combo)
        self.layout.addWidget(QLabel("Party Size:"))
        self.layout.addWidget(self.party_size_edit)
        self.layout.addWidget(QLabel("Table Number:"))
        self.layout.addWidget(self.table_number_combo)

        # Add labels for table ID and seats
        self.table_ID_label = QLabel()
        self.table_seats_label = QLabel()
        self.layout.addWidget(self.table_ID_label)
        self.layout.addWidget(self.table_seats_label)

        self.layout.addWidget(self.update_reservation_button)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

        self.load_reservation_data(reservation_data)

        self.table_number_combo.currentIndexChanged.connect(self.update_table_id_and_seats_label)

    def load_reservation_data(self, reservation_data):
        self.reservation_id = reservation_data['rs_reservation_id']
        self.customer_name_edit.setText(reservation_data['rs_name'])
        self.reservation_date_calendar.setSelectedDate(reservation_data['rs_reservation_date'])
        time = reservation_data['rs_reservation_time'].seconds // 3600, reservation_data['rs_reservation_time'].seconds // 60 % 60
        self.populate_reservation_time_combo(f"{time[0]:02d}:{time[1]:02d}")
        self.party_size_edit.setText(str(reservation_data['rs_party_size']))
        self.populate_table_number_combo(reservation_data['rs_table_id'])

    def populate_reservation_time_combo(self, selected_time):
        self.reservation_time_combo.clear()
        for hour in range(17, 24):
            for minute in range(0, 60, 15):
                self.reservation_time_combo.addItem(f"{hour:02d}:{minute:02d}")
        self.reservation_time_combo.setCurrentText(selected_time)

    def populate_table_number_combo(self, selected_table_id):
        self.table_number_combo.clear()
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT rs_table_id, rs_number, rs_status FROM tables")
                for table in cursor:
                    table_id, number, status = table['rs_table_id'], table['rs_number'], table['rs_status']
                    self.table_number_combo.addItem(f"Table {number} -- {status}", table_id)
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred while loading tables: {e}")
        self.table_number_combo.setCurrentIndex(self.table_number_combo.findData(selected_table_id))

    def confirm_update_reservation(self):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to update the reservation?")
        confirm_dialog.setWindowTitle("Confirm Update")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.buttonClicked.connect(self.update_reservation_on_confirm)
        confirm_dialog.exec()

    def update_reservation_on_confirm(self, button):
        button_answer = button.text()
        if button_answer == "&Yes":
            self.update_reservation()

    def update_reservation(self):
        selected_table_id = self.table_number_combo.currentData()
        if selected_table_id is None:
            QMessageBox.warning(self, "Input Error", "Please select a table number.")
            return

        new_reservation_date = self.reservation_date_calendar.selectedDate().toString("yyyy-MM-dd")
        new_reservation_time = self.reservation_time_combo.currentText()
        new_party_size = int(self.party_size_edit.text())

        try:
            with self.db_connection.cursor() as cursor:
                # Check if the selected table is already reserved
                cursor.execute("SELECT rs_status FROM tables WHERE rs_table_id = %s", (selected_table_id,))
                table_status = cursor.fetchone()['rs_status']
                if table_status == 'reserved':
                    QMessageBox.warning(self, "Table Reserved",
                                        "This table is already reserved. Please select another table.")
                    return

                # Get the previous table ID associated with the reservation
                cursor.execute("SELECT rs_table_id FROM reservation WHERE rs_reservation_id = %s", (self.reservation_id,))
                previous_table_id = cursor.fetchone()['rs_table_id']

                # Update reservation with new table ID
                cursor.execute("UPDATE reservation SET rs_table_id = %s, rs_reservation_date = %s, "
                               "rs_reservation_time = %s, rs_party_size = %s "
                               "WHERE rs_reservation_id = %s",
                               (selected_table_id, new_reservation_date, new_reservation_time,
                                new_party_size, self.reservation_id))

                # Update previous table status to 'available'
                cursor.execute("UPDATE tables SET rs_status = 'available' WHERE rs_table_id = %s", (previous_table_id,))

                # Update new table status to 'reserved'
                cursor.execute("UPDATE tables SET rs_status = 'reserved' WHERE rs_table_id = %s", (selected_table_id,))

            self.db_connection.commit()

            QMessageBox.information(self, "Success", "Reservation updated successfully.")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def close_dialog(self):
        self.close()
        self.dialogClosed.emit()

    def update_table_id_and_seats_label(self, index):
        if index >= 0:
            table_id = self.table_number_combo.itemData(index)
            if table_id is not None:
                try:
                    with self.db_connection.cursor() as cursor:
                        cursor.execute("SELECT rs_seats FROM tables WHERE rs_table_id = %s", (table_id,))
                        result = cursor.fetchone()
                        if result:
                            self.table_ID_label.setText(f"Table ID: {table_id}")
                            self.table_seats_label.setText(f"Table Seats: {result['rs_seats']}")
                        else:
                            self.table_ID_label.clear()
                            self.table_seats_label.clear()
                except Exception as e:
                    QMessageBox.warning(self, "Database Error", f"An error occurred while loading table seats: {e}")
                    self.table_ID_label.clear()
                    self.table_seats_label.clear()
            else:
                self.table_ID_label.clear()
                self.table_seats_label.clear()
        else:
            self.table_ID_label.clear()
            self.table_seats_label.clear()

class ReservationManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reservation Management")
        self.setGeometry(100, 100, 950, 600)
        self.db_connection = self.create_db_connection()
        self.initUI()
        self.load_reservations()
        self.add_reservation_window = None

    def create_db_connection(self):
        return connect(host='localhost', user='dbadmin', password='dbadmin', database='restaurant',
                       cursorclass=cursors.DictCursor)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["reservation_id", "Name", "reservation_date", "reservation_time", "party_size", "TableID", None, None])
        self.layout.addWidget(self.table)

        self.add_reservation_layout = QHBoxLayout()
        self.add_reservation_button = QPushButton("Add Reservation")
        self.add_reservation_button.clicked.connect(self.add_reservation)
        self.add_reservation_layout.addWidget(self.add_reservation_button)
        self.layout.addLayout(self.add_reservation_layout)
        self.setLayout(self.layout)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_reservations)
        self.refresh_timer.start(1000)

    def load_reservations(self):
        self.table.setRowCount(0)
        today_date = datetime.now().date()
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT rs_reservation_id, customer.rs_name, rs_reservation_date, rs_reservation_time, rs_party_size, rs_table_id FROM reservation "
                    "JOIN customer ON reservation.rs_customer_id = customer.rs_customer_id "
                    "WHERE rs_reservation_date = %s", (today_date,))
                for row_number, row_data in enumerate(cursor):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data.values()):
                        self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.table.setCellWidget(row_number, 6, self.create_update_button(row_data))
                    self.table.setCellWidget(row_number, 7, self.create_delete_button(row_data['rs_reservation_id']))
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def create_update_button(self, reservation_data):
        btn_update = QPushButton('Update')
        btn_update.clicked.connect(lambda: self.open_update_reservation_dialog(reservation_data))
        return btn_update

    def create_delete_button(self, reservation_id):
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.confirm_delete_reservation(reservation_id))
        return btn_delete

    def confirm_delete_reservation(self, reservation_id):
        confirm_dialog = QMessageBox()
        confirm_dialog.setIcon(QMessageBox.Question)
        confirm_dialog.setText("Are you sure you want to delete the reservation?")
        confirm_dialog.setWindowTitle("Confirm Delete")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.buttonClicked.connect(lambda button: self.delete_reservation(reservation_id, button))
        confirm_dialog.exec()

    def delete_reservation(self, reservation_id, button):
        if button.text() == "&Yes":
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("DELETE FROM reservation WHERE rs_reservation_id = %s", (reservation_id,))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Reservation deleted successfully.")
                    self.load_reservations()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def open_update_reservation_dialog(self, reservation_data):
        dialog = UpdateReservationDialog(reservation_data, self.db_connection, self)
        dialog.dialogClosed.connect(self.load_reservations)
        dialog.exec()

    def add_reservation(self):
        if not self.add_reservation_window:
            self.add_reservation_window = CustomerWindow()
        self.add_reservation_window.show()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    window = ReservationManagement()
    window.show()
    app.exec()
