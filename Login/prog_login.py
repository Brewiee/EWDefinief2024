import bcrypt
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import QEvent, QSize, QTimer
import pymysql
from subprocess import Popen
from datetime import datetime
from stylesheet_login import object_stylesheet
from main_menu_superadmin import main_menu_superadmin
from main_menu_cashregister import main_menu_cashregister
from main_menu_restaurant import main_menu_restaurant
from main_menu_vending import main_menu_vending
from subprocess import Popen



class LoginDatabaseFunctions(QMainWindow):
    def __init__(self):

        super().__init__()
        self.init_ui()
        self.user_activity_timer = QTimer()
        self.user_activity_timer.setInterval(5000)
        self.user_activity_timer.timeout.connect(self.logout_due_to_inactivity)
        self.last_activity_time = datetime.now()
        self.current_sub_process = None

    def hash_password(self, password, salt):
        """Hashes the password with bcrypt algorithm and salt."""
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def connect_to_database(self):
        try:
            conn = pymysql.connect(
                host="localhost",
                user="dbadmin",
                password="dbadmin",
                database="users"
            )
            return conn
        except pymysql.Error as err:
            print("Error:", err)
            return None

    def init_ui(self):
        self.setWindowTitle("General login")
        self.setGeometry(100, 100, 300, 250)
        self.setStyleSheet(object_stylesheet.central_widget())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setup_username_section(layout)
        self.setup_password_section(layout)
        self.setup_module_selection(layout)
        self.setup_login_button(layout)
        self.setup_error_label(layout)

    def setup_username_section(self, layout):
        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.username_edit.editingFinished.connect(self.check_username)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        self.username_edit.setStyleSheet(object_stylesheet.line_edit())
        self.username_label.setStyleSheet(object_stylesheet.label())

    def setup_password_section(self, layout):
        self.password_label = QLabel("Password:")
        password_layout = QHBoxLayout()
        layout.addWidget(self.password_label)
        layout.addLayout(password_layout)
        self.password_label.setStyleSheet(object_stylesheet.label())

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_edit)
        self.password_edit.setStyleSheet(object_stylesheet.line_edit())

        self.setup_password_visibility_button(password_layout)

    def setup_password_visibility_button(self, layout):
        self.password_visibility_button = QPushButton()
        self.password_visibility_button.setIcon(QIcon("eye_icon1.png"))
        self.password_visibility_button.setCheckable(True)
        self.password_visibility_button.setIconSize(QSize(24, 24))
        self.password_visibility_button.toggled.connect(self.toggle_password_visibility)
        self.password_visibility_button.setStyleSheet(object_stylesheet.pushbutton())
        self.password_visibility_button.installEventFilter(self)
        layout.addWidget(self.password_visibility_button)
        self.password_visibility_button.setStyleSheet(object_stylesheet.pushbutton())

    def setup_module_selection(self, layout):
        self.options_label = QLabel("Choose your module:")
        self.options_label.setStyleSheet(object_stylesheet.label())
        self.options_combo = QComboBox()
        self.options_combo.addItem("Select module")
        self.options_combo.currentIndexChanged.connect(self.get_user_type)
        layout.addWidget(self.options_label)
        layout.addWidget(self.options_combo)
        self.options_combo.setStyleSheet(object_stylesheet.combo_box())

    def setup_login_button(self, layout):
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        self.login_button.setStyleSheet(object_stylesheet.pushbutton())

    def setup_error_label(self, layout):
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red")
        layout.addWidget(self.error_label)
        layout.addStretch()

    def eventFilter(self, obj, event):
        if obj == self.password_visibility_button:
            if event.type() == QEvent.HoverEnter:
                self.password_visibility_button.setIcon(QIcon("eye_icon1-inverted.png"))
            elif event.type() == QEvent.HoverLeave:
                self.password_visibility_button.setIcon(QIcon("eye_icon1.png"))
        return super().eventFilter(obj, event)

    def check_username(self):
        username = self.username_edit.text()
        conn = self.connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM userinfo WHERE username = %s"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                conn.close()
                if user:
                    self.error_label.setText("")
                    self.password_edit.setEnabled(True)
                    self.password_edit.setFocus()
                    self.populate_options()
                else:
                    self.error_label.setText("Please enter a valid username")
                    self.password_edit.clear()
                    self.password_edit.setEnabled(False)
                    self.options_combo.clear()
            except pymysql.Error as err:
                print("Error:", err)
        else:
            print("Failed to connect to the database.")

    def toggle_password_visibility(self):
        mode = QLineEdit.Normal if self.password_visibility_button.isChecked() else QLineEdit.Password
        self.password_edit.setEchoMode(mode)

    def populate_options(self):
        username = self.username_edit.text()
        conn = self.connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM userinfo WHERE username = %s"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                if user:
                    self.options_combo.clear()
                    self.options_combo.addItem("Select module")
                    column_names = [column[0] for column in cursor.description]  # Modified line
                    permissions = [self.get_permission_label(col) for col in column_names if
                                   col.startswith('perm') and user[column_names.index(col)] != 1]
                    if len(permissions) == 1:
                        self.options_combo.addItem(permissions[0])
                    else:
                        for permission in permissions:
                            self.options_combo.addItem(permission)
                    if len(permissions) > 1:
                        self.options_combo.setCurrentIndex(0)
                        self.error_label.setText("Please select a module")
            except pymysql.Error as err:
                print("Error:", err)
            finally:
                conn.close()
        else:
            print("Failed to connect to the database.")

    def get_permission_label(self, column_name):
        return {
            "perm_vend": "Vending",
            "perm_rest": "Restaurant",
            "perm_cr": "Cash register",
            "perm_super": "SuperAdmin"
        }.get(column_name)

    def get_user_type(self):
        selected_module = self.options_combo.currentText()
        if selected_module != "Select module":
            conn = self.connect_to_database()
            if conn:
                try:
                    cursor = conn.cursor()
                    column_name = {"Vending": "perm_vend", "Restaurant": "perm_rest", "Cash register": "perm_cr", "SuperAdmin": "perm_super"}.get(selected_module)
                    if column_name:
                        query = f"SELECT `{column_name}` FROM userinfo WHERE username = %s"
                        cursor.execute(query, (self.username_edit.text(),))
                        result = cursor.fetchone()
                        self.user_type = result[0] if result else None
                    else:
                        self.user_type = None
                except pymysql.Error as err:
                    print("Error:", err)
                finally:
                    conn.close()
            else:
                print("Failed to connect to the database.")

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Retrieve the selected module from the combo box
        selected_module = self.options_combo.currentText()

        # Check if a module is selected
        if not selected_module or selected_module == "Select module":
            self.error_label.setText("Please select a module")
            return

        conn = self.connect_to_database()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT * FROM userinfo WHERE username = %s"
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                if user:
                    stored_password_hash = user[2]
                    salt = user[3]  # Assuming salt is stored in the fourth column
                    if bcrypt.checkpw(password.encode(), stored_password_hash.encode()):
                        # Terminate the current subprocess if exists
                        if self.current_sub_process:
                            self.current_sub_process.terminate()
                        # Start the subprocess corresponding to the selected module
                        if selected_module == "Vending":
                            self.current_sub_process = Popen(["python", "../vending/main.py"])
                        elif selected_module == "Restaurant":
                            self.current_sub_process = Popen(["python", "main_menu_restaurant.py"])
                        elif selected_module == "Cash register":
                            self.current_sub_process = Popen(["python", "main_menu_cashregister.py"])
                        elif selected_module == "SuperAdmin":
                            self.current_sub_process = Popen(["python", "main_menu_superadmin.py"])
                        else:
                            QMessageBox.warning(self, "Login", "Invalid module selected.")
                            return
                        self.hide()  # Hide the login window after successful login
                        # Reset the timer whenever there's user activity
                        self.last_activity_time = datetime.now()
                        self.user_activity_timer.start()
                    else:
                        QMessageBox.warning(self, "Login", "Incorrect username or password.")
                else:
                    QMessageBox.warning(self, "Login", "Incorrect username or password.")
            except pymysql.Error as err:
                print("Error:", err)
            finally:
                conn.close()
        else:
            print("Failed to connect to the database.")

    def logout_due_to_inactivity(self):
        # Calculate the time difference between now and the last activity time
        time_diff = (datetime.now() - self.last_activity_time).seconds
        if time_diff >= 300:  # if the user has been inactive for 3 seconds
            self.user_activity_timer.stop()
            # Terminate the current subprocess if exists
            if self.current_sub_process:
                self.current_sub_process.terminate()

            self.password_edit.setText("")
            self.username_edit.setText("")
            # Show the login window again
            self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(object_stylesheet.pushbutton())
    login_window = LoginDatabaseFunctions()
    login_window.show()
    sys.exit(app.exec())
