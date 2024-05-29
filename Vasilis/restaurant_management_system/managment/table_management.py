import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
                               QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QComboBox)
from pymysql import connect, cursors


class TableManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Table Management")
        self.setGeometry(100, 100, 950, 600)
        self.db_connection = self.create_db_connection()
        self.initUI()
        self.load_tables()

    def create_db_connection(self):
        return connect(host='localhost', user='dbadmin', password='dbadmin', database='restaurant',
                       cursorclass=cursors.DictCursor)

    def initUI(self):
        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)  # Columns for TableID, Number, Seats, Status, Update, Delete
        self.table_widget.setHorizontalHeaderLabels(
            ["TableID", "Number", "Seats", "Status", "Update", "Delete"])
        self.layout.addWidget(self.table_widget)

        # Add table form setup
        self.add_table_layout = QHBoxLayout()
        self.number_input = QLineEdit()
        self.seats_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["available", "occupied", "reserved", "locked"])

        self.add_table_button = QPushButton("Add Table")
        self.add_table_button.clicked.connect(self.add_table)

        # Adding widgets to the layout
        self.add_table_layout.addWidget(QLabel("Number:"))
        self.add_table_layout.addWidget(self.number_input)
        self.add_table_layout.addWidget(QLabel("Seats:"))
        self.add_table_layout.addWidget(self.seats_input)
        self.add_table_layout.addWidget(QLabel("Status:"))
        self.add_table_layout.addWidget(self.status_input)
        self.add_table_layout.addWidget(self.add_table_button)

        self.layout.addLayout(self.add_table_layout)
        self.setLayout(self.layout)

    def load_tables(self):
        self.table_widget.setRowCount(0)
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tables")
                for row_number, row_data in enumerate(cursor):
                    self.table_widget.insertRow(row_number)
                    for column_number, data in enumerate(row_data.values()):
                        self.table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.table_widget.setCellWidget(row_number, 4, self.create_update_button(row_data['rs_table_id']))
                    self.table_widget.setCellWidget(row_number, 5, self.create_delete_button(row_data['rs_table_id']))

        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def create_update_button(self, tableID):
        btn_update = QPushButton('Update')
        btn_update.clicked.connect(lambda: self.open_update_dialog(tableID))
        return btn_update

    def create_delete_button(self, tableID):
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.delete_table(tableID))
        return btn_delete

    def add_table(self):
        number = self.number_input.text()
        seats = self.seats_input.text()
        status = self.status_input.currentText()

        if not all([number, seats, status]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        confirmation = QMessageBox.question(self, "Confirm Addition",
                                            "Are you sure you want to add this table?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("SELECT MAX(rs_table_id) AS max_id FROM tables")
                    max_id = cursor.fetchone()['max_id']
                    new_table_id = 1 if max_id is None else max_id + 1

                    cursor.execute(
                        "INSERT INTO tables (rs_table_id, rs_number, rs_seats, rs_status) VALUES (%s, %s, %s, %s)",
                        (new_table_id, number, seats, status))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Table added successfully.")
                    self.number_input.clear()
                    self.seats_input.clear()
                    self.status_input.setCurrentIndex(0)
                    self.load_tables()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "Table addition cancelled.")

    def delete_table(self, tableID):
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            "Are you sure you want to delete this table?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("DELETE FROM tables WHERE rs_table_id = %s", (tableID,))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Table deleted successfully.")
                    self.load_tables()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "Table deletion cancelled.")

    def open_update_dialog(self, tableID):
        dialog = EditTableDialog(tableID, self.db_connection)
        dialog.exec_()
        self.load_tables()


class EditTableDialog(QDialog):
    def __init__(self, tableID, db_connection, parent=None):
        super().__init__(parent)
        self.tableID = tableID
        self.db_connection = db_connection
        self.setWindowTitle('Edit Table')
        self.setGeometry(100, 100, 300, 200)
        self.initUI()
        self.load_table_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.number_input = QLineEdit()
        self.seats_input = QLineEdit()
        self.status_input = QComboBox()  # Change to QComboBox

        form_layout.addRow("Number:", self.number_input)
        form_layout.addRow("Seats:", self.seats_input)
        form_layout.addRow("Status:", self.status_input)  # Add QComboBox

        self.status_input.addItems(["available", "occupied", "reserved", "locked"])  # Add items to QComboBox

        self.update_button = QPushButton("Update Table")
        self.update_button.clicked.connect(self.update_table)
        layout.addLayout(form_layout)
        layout.addWidget(self.update_button)

    def load_table_data(self):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT rs_number, rs_seats, rs_status FROM tables WHERE rs_table_id = %s", (self.tableID,))
                table = cursor.fetchone()
                if table:
                    self.number_input.setText(str(table['rs_number']))
                    self.seats_input.setText(str(table['rs_seats']))
                    # Set the current index of the combobox based on the status value
                    index = self.status_input.findText(table['rs_status'])
                    if index >= 0:
                        self.status_input.setCurrentIndex(index)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load table data: {e}")

    def update_table(self):
        number = self.number_input.text()
        seats = self.seats_input.text()
        status = self.status_input.currentText()  # Get the selected text from the combobox

        if not all([number, seats, status]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        confirmation = QMessageBox.question(self, "Confirm Update",
                                            "Are you sure you want to update this table?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("UPDATE tables SET rs_number=%s, rs_seats=%s, rs_status=%s WHERE rs_table_id=%s",
                                   (number, seats, status, self.tableID))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "Table updated successfully.")
                    self.accept()  # Close the dialog
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
                print(e)
        else:
            QMessageBox.information(self, "Cancelled", "Table update cancelled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = TableManagementWidget()
    window.show()
    sys.exit(app.exec())
