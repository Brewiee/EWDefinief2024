import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel,
                               QTableWidget, QTableWidgetItem, QMessageBox, QDialog, QFormLayout, QComboBox)
from PySide6.QtCore import QTimer
from pymysql import connect, cursors

class UserManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(100, 100, 950, 600)
        self.db_connection = self.create_db_connection()
        self.initUI()
        self.load_users()

    def create_db_connection(self):
        return connect(host='localhost', user='dbadmin', password='dbadmin', database='restaurantV2',
                       cursorclass=cursors.DictCursor)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["UserID", "Username", "Password", "Role", "Full Name", "Update", "Delete"])
        self.layout.addWidget(self.table)

        self.add_user_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.role_input = QComboBox()  # Change to QComboBox
        self.role_input.addItems([None, "admin", "staff"])  # Add choices
        self.fullname_input = QLineEdit()

        self.add_user_button = QPushButton("Add User")
        self.add_user_button.clicked.connect(self.add_user)

        self.add_user_layout.addWidget(QLabel("Username:"))
        self.add_user_layout.addWidget(self.username_input)
        self.add_user_layout.addWidget(QLabel("Password:"))
        self.add_user_layout.addWidget(self.password_input)
        self.add_user_layout.addWidget(QLabel("Role:"))
        self.add_user_layout.addWidget(self.role_input)
        self.add_user_layout.addWidget(QLabel("Full Name:"))
        self.add_user_layout.addWidget(self.fullname_input)
        self.add_user_layout.addWidget(self.add_user_button)

        self.layout.addLayout(self.add_user_layout)
        self.setLayout(self.layout)

        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.load_users)
        self.refresh_timer.start(1000)

    def load_users(self):
        self.table.setRowCount(0)
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Users")
                for row_number, row_data in enumerate(cursor):
                    self.table.insertRow(row_number)
                    for column_number, data in enumerate(row_data.values()):
                        self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.table.setCellWidget(row_number, 5, self.create_update_button(row_data['UserID']))
                    self.table.setCellWidget(row_number, 6, self.create_delete_button(row_data['UserID']))
        except Exception as e:
            QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def create_update_button(self, userID):
        btn_update = QPushButton('Update')
        btn_update.clicked.connect(lambda: self.open_update_dialog(userID))
        return btn_update

    def create_delete_button(self, userID):
        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(lambda: self.delete_user(userID))
        return btn_delete

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.text()
        fullname = self.fullname_input.text()

        if not all([username, password, role, fullname]):
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        confirmation = QMessageBox.question(self, "Confirm User Creation",
                                             "Are you sure you want to create this user account?",
                                             QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("INSERT INTO Users (Username, Password, Role, FullName) VALUES (%s, %s, %s, %s)",
                                   (username, password, role, fullname))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "User added successfully.")
                    self.load_users()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "User creation cancelled.")

    def delete_user(self, userID):
        confirmation = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this user?",
                                             QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Users WHERE UserID = %s", (userID,))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "User deleted successfully.")
                    self.load_users()
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")

    def open_update_dialog(self, userID):
        confirmation = QMessageBox.question(self, "Confirm Update",
                                             "Are you sure you want to update this user?",
                                             QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            dialog = EditUserDialog(userID, self.db_connection)
            dialog.exec_()
            self.load_users()
        else:
            QMessageBox.information(self, "Cancelled", "User update cancelled.")

class EditUserDialog(QDialog):
    def __init__(self, userID, db_connection, parent=None):
        super().__init__(parent)
        self.userID = userID
        self.db_connection = db_connection
        self.setWindowTitle('Edit User')
        self.setGeometry(100, 100, 300, 200)
        self.initUI()
        self.load_user_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.role_input = QComboBox()
        self.role_input.addItems(["admin", "staff"])
        self.fullname_input = QLineEdit()

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Role:", self.role_input)
        form_layout.addRow("Full Name:", self.fullname_input)

        self.update_button = QPushButton("Update User")
        self.update_button.clicked.connect(self.update_user)
        layout.addLayout(form_layout)
        layout.addWidget(self.update_button)

    def load_user_data(self):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT Username, Password, Role, FullName FROM Users WHERE UserID = %s", (self.userID,))
                user = cursor.fetchone()
                if user:
                    self.username_input.setText(user['Username'])
                    self.password_input.setText(user['Password'])
                    self.role_input.addItem(user['Role'])
                    self.fullname_input.setText(user['FullName'])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load user data: {e}")

    def update_user(self):
        confirmation = QMessageBox.question(self, "Confirm Update",
                                             "Are you sure you want to update this user?",
                                             QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            username = self.username_input.text()
            password = self.password_input.text()
            # pull the choice of the combobox already viewd
            role = self.role_input.currentText()
            fullname = self.fullname_input.text()

            if not all([username, password, role, fullname]):
                QMessageBox.warning(self, "Input Error", "All fields are required.")
                return

            try:
                with self.db_connection.cursor() as cursor:
                    cursor.execute("UPDATE Users SET Username=%s, Password=%s, Role=%s, FullName=%s WHERE UserID=%s",
                                   (username, password, role, fullname, self.userID))
                    self.db_connection.commit()
                    QMessageBox.information(self, "Success", "User updated successfully.")
                    self.accept()  # Close the dialog
            except Exception as e:
                QMessageBox.warning(self, "Database Error", f"An error occurred: {e}")
        else:
            QMessageBox.information(self, "Cancelled", "User update cancelled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = UserManagement()
    window.show()
    sys.exit(app.exec())
