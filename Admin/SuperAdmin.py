from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGroupBox, \
    QMessageBox, QFileDialog, QDialog, QDialogButtonBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from datetime import datetime
import pymysql
import os
import subprocess

# Variables
ICONS_FOLDER = "../icons/"
Hname = "localhost"
Uname = "dbadmin"
Pword = "dbadmin"
db_nameCR = "CashRegister"
db_nameVD = "Vending"
db_nameRS = "Restaurant"
db_nameUS = "Users"

class DatabaseManager:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def check_database_exists(self, db_name):
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            return cursor.fetchone() is not None
        except pymysql.Error as e:
            print(f"Error checking database existence: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def create_database(self, db_name):
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            return True
        except pymysql.Error as e:
            print(f"Error creating database '{db_name}': {e}")
            return False
        finally:
            if conn:
                conn.close()

    def execute_sql_script(self, db_name, script_path=None):
        if script_path is None:
            script_path = os.path.join("Data", f"table_queries_{db_name}.sql")
            if not os.path.exists(script_path):
                print(f"Table creation script for '{db_name}' does not exist.")
                return False

        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db_name
            )
            cursor = conn.cursor()
            with open(script_path, "r") as file:
                table_queries = file.read().split(";")
            table_queries.pop()
            for query in table_queries:
                cursor.execute(query)
            conn.commit()
            print(f"Tables for {db_name} were created successfully.")
            return True
        except pymysql.Error as e:
            print(f"Error executing SQL script for '{db_name}': {e}")
            return False
        finally:
            if conn:
                conn.close()

    def check_table_exists(self, db_name, table_name):
        conn = None
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=db_name
            )
            cursor = conn.cursor()
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            return cursor.fetchone() is not None
        except pymysql.Error as e:
            print(f"Error checking table existence: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def add_dummy_data(self, db_name, script_path):
        return self.execute_sql_script(db_name, script_path)

class RestoreBackup:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def select_backup_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(None, "Select Backup File", "", "SQL Files (*.sql)", options=options)
        return file_name

    def restore_backup(self, db_name):
        if not self.db_manager.check_database_exists(db_name):
            self.db_manager.create_database(db_name)
            print(f"Database '{db_name}' created successfully.")

        # Check if necessary tables exist
        necessary_tables = ["category", "product"]  # Add more tables as needed
        missing_tables = []
        for table in necessary_tables:
            if not self.db_manager.check_table_exists(db_name, table):
                missing_tables.append(table)

        if missing_tables:
            print(f"Tables {missing_tables} do not exist in '{db_name}'. Creating them now...")
            # You need to replace `table_creation_script.sql` with the script that creates the necessary tables
            if not self.db_manager.execute_sql_script(db_name):
                print("Error creating tables. Aborting restore operation.")
                return

        conn = None
        try:
            conn = pymysql.connect(
                host=self.db_manager.host,
                user=self.db_manager.user,
                password=self.db_manager.password,
                database=db_name
            )
            cursor = conn.cursor()

            # Disable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS=0")

            # Select backup file
            backup_file = self.select_backup_file()
            if not backup_file:
                print("No backup file selected. Operation cancelled.")
                return

            # Check if the selected backup file exists
            if not os.path.exists(backup_file):
                print("Selected backup file does not exist. Operation cancelled.")
                return

            # Read the backup file
            with open(backup_file, "r") as f:
                sql_commands = f.read().split(';')

            # Execute each SQL command
            for command in sql_commands:
                if command.strip():  # Check if the command is not empty
                    try:
                        cursor.execute(command)

                        # Check for foreign key constraint errors
                        if "foreign key" in command.lower():
                            self.create_index_for_foreign_key(cursor, command)

                    except pymysql.IntegrityError as e:
                        print(f"Error restoring data to '{db_name}' database: {e}")
                        print("Skipping duplicate entry.")
                    except pymysql.Error as e:
                        print(f"Error executing SQL command: {e}")
                        print(f"SQL command: {command}")
                        print("Skipping this command.")

            conn.commit()
            print(f"Backup restored for '{db_name}' database.")
        except pymysql.Error as e:
            print(f"Error restoring backup for '{db_name}': {e}")
        finally:
            if conn:
                # Re-enable foreign key checks
                cursor.execute("SET FOREIGN_KEY_CHECKS=1")
                conn.close()

    def create_index_for_foreign_key(self, cursor, command):
        # Extract foreign key details from SQL command
        start_index = command.lower().find("foreign key") + len("foreign key")
        end_index = command.find("references")
        foreign_key_statement = command[start_index:end_index].strip()

        # Extract table and column names
        referenced_table = foreign_key_statement.split("(")[1].split(")")[0].strip()
        referenced_column = foreign_key_statement.split("(")[1].split(")")[1].split()[0].strip()

        # Check if the index already exists
        index_name = f"idx_{referenced_table}_{referenced_column}"
        cursor.execute(f"SHOW INDEX FROM {referenced_table} WHERE Key_name='{index_name}'")
        index_exists = cursor.fetchone() is not None

        # Create index if it doesn't exist
        if not index_exists:
            cursor.execute(f"ALTER TABLE {referenced_table} ADD INDEX {index_name} ({referenced_column})")
            print(f"Index '{index_name}' created for '{referenced_table}.{referenced_column}'")

class DropTablesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Drop Tables")
        self.setModal(True)
        self.setStyleSheet("background-color: #333333; color: white;")

        main_layout = QVBoxLayout(self)

        label = QLabel("Are you sure you want to drop all user-created databases?")
        label.setStyleSheet("color: white;")
        main_layout.addWidget(label)

        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout.addWidget(button_box)

class ManagementDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Management Dashboard')
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Set dark mode background color
        self.setStyleSheet("background-color: #333333; color: white;")

        # Create a QHBoxLayout for the boxes
        boxes_layout = QHBoxLayout()
        boxes_layout.setAlignment(Qt.AlignCenter)

        # Create "Create" box
        create_box = self.create_button_box("Create", [
            {"text": "Cash Register", "icon": "create_cash_register.png", "function": self.create_cash_register},
            {"text": "Vending", "icon": "create_vending.png", "function": self.create_vending},
            {"text": "Restaurant", "icon": "create_restaurant.png", "function": self.create_restaurant},
            {"text": "Users", "icon": "create_users.png", "function": self.create_users},
            {"text": "All", "icon": "create_all.png", "function": self.create_all},
        ])
        boxes_layout.addWidget(create_box)

        # Create "Backup" box
        backup_box = self.create_button_box("Backup", [
            {"text": "Cash Register", "icon": "backup_cash_register.png", "function": self.backup_cash_register},
            {"text": "Vending", "icon": "backup_vending.png", "function": self.backup_vending},
            {"text": "Restaurant", "icon": "backup_restaurant.png", "function": self.backup_restaurant},
            {"text": "Users", "icon": "backup_users.png", "function": self.backup_users},
            {"text": "All", "icon": "backup_all.png", "function": self.backup_all},
        ])
        boxes_layout.addWidget(backup_box)

        # Create "Restore" box
        restore_box = self.create_button_box("Restore", [
            {"text": "Cash Register", "icon": "restore_cash_register.png", "function": self.restore_cash_register},
            {"text": "Vending", "icon": "restore_vending.png", "function": self.restore_vending},
            {"text": "Restaurant", "icon": "restore_restaurant.png", "function": self.restore_restaurant},
            {"text": "Users", "icon": "restore_users.png", "function": self.restore_users},
            {"text": "All", "icon": "restore_all.png", "function": self.restore_all},
        ])
        boxes_layout.addWidget(restore_box)

        # Create "Drop" box
        drop_box = self.create_button_box("Admin functions", [
            {"text": "Drop Tables", "icon": "drop.png", "function": self.drop_tables},
            {"text": "Panic button", "icon": "panic.png", "function": self.panic},
            {"text": "DBManager button", "icon": "DBManager.png", "function": self.dbmanager},
        ])
        boxes_layout.addWidget(drop_box)

        # Add the boxes layout to the main layout
        main_layout.addLayout(boxes_layout)

        # Initialize DatabaseManager instance
        self.db_manager = DatabaseManager(Hname, Uname, Pword)

        # Initialize RestoreBackup instance
        self.restore_backup = RestoreBackup(self.db_manager)

    def create_button_box(self, title, buttons_data):
        box = QGroupBox(title)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        for btn_data in buttons_data:
            button = QPushButton()
            button.setIcon(QIcon(ICONS_FOLDER + btn_data["icon"]))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(150, 150)
            button.clicked.connect(btn_data["function"])
            button.setStyleSheet("background-color: #33333; color: white; border: none;")

            label = QLabel(btn_data["text"])
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: white;")

            layout.addWidget(button)
            layout.addWidget(label)

        box.setLayout(layout)
        return box

    def create_database(self, db_name):
        try:
            conn = pymysql.connect(host=Hname, user=Uname, password=Pword)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            QMessageBox.information(self, "Success", f"Database '{db_name}' created successfully!")
            return True
        except pymysql.Error as e:
            print(f"Error creating database '{db_name}': {e}")
            QMessageBox.critical(self, "Error", f"Error creating database '{db_name}': {e}")
            return False
        finally:
            if conn:
                conn.close()

    def execute_sql_script(self, db_name, script_path):
        if not os.path.exists(script_path):
            print(f"Table creation script for '{db_name}' does not exist.")
            return False

        conn = None
        try:
            conn = pymysql.connect(
                host=self.db_manager.host,
                user=self.db_manager.user,
                password=self.db_manager.password,
                database=db_name
            )
            cursor = conn.cursor()
            with open(script_path, "r") as file:
                table_queries = file.read().split(";")
            table_queries.pop()
            for query in table_queries:
                cursor.execute(query)
            conn.commit()
            print(f"Tables for {db_name} were created successfully.")
            return True
        except pymysql.Error as e:
            print(f"Error executing SQL script for '{db_name}': {e}")
            return False
        finally:
            if conn:
                conn.close()

    def add_dummy_data(self, db_name, data_path):
        try:
            conn = pymysql.connect(host=Hname, user=Uname, password=Pword, database=db_name)
            with open(data_path, 'r', encoding='utf-8') as file:  # Specify encoding here
                cursor = conn.cursor()
                for line in file:
                    sql_statement = line.strip()
                    if sql_statement:
                        cursor.execute(sql_statement)
            conn.commit()
            print("Dummy data added to the database.")
        except pymysql.Error as e:
            print(f"Error adding dummy data to '{db_name}' database: {e}")
        finally:
            if conn:
                conn.close()

    def ask_for_dummy_data(self, db_name):
        message_box = QMessageBox()
        choice = message_box.question(self, "Add Dummy Data",
                                      f"Do you want to add dummy data to the {db_name} database?",
                                      QMessageBox.Yes | QMessageBox.No)
        return choice == QMessageBox.Yes

    def create_cash_register(self):
        db_name = db_nameCR
        if self.check_database_exists(db_name):
            QMessageBox.information(self, "Database Exists",
                                    f"The '{db_name}' database already exists. I did not create a new database.")
            return

        if self.create_database(db_name):
            if self.execute_sql_script(db_name, os.path.join("Data", f"table_queries_{db_name}.sql")):
                if self.ask_for_dummy_data(db_name):
                    self.add_dummy_data(db_name, os.path.join("Data", f'Dummy_Data_{db_name}.sql'))

    def create_vending(self):
        db_name = db_nameVD
        if self.check_database_exists(db_name):
            QMessageBox.information(self, "Database Exists",
                                    f"The '{db_name}' database already exists. I did not create a new database.")
            return

        if self.create_database(db_name):
            if self.execute_sql_script(db_name, os.path.join("Data", f"table_queries_{db_name}.sql")):
                if self.ask_for_dummy_data(db_name):
                    self.add_dummy_data(db_name, os.path.join("Data", f'Dummy_Data_{db_name}.sql'))

    def create_restaurant(self):
        # First, create the users database
        self.create_users()

        db_name = db_nameRS
        if self.check_database_exists(db_name):
            QMessageBox.information(self, "Database Exists",
                                    f"The '{db_name}' database already exists. I did not create a new database.")
            return

        if self.create_database(db_name):
            if self.execute_sql_script(db_name, os.path.join("Data", f"table_queries_{db_name}.sql")):
                if self.ask_for_dummy_data(db_name):
                    self.add_dummy_data(db_name, os.path.join("Data", f'Dummy_Data_{db_name}.sql'))

    def create_users(self):
        db_name = db_nameUS
        if self.check_database_exists(db_name):
            QMessageBox.information(self, "Database Exists",
                                    f"The '{db_name}' database already exists. I did not create a new database.")
            return

        if self.create_database(db_name):
            if self.execute_sql_script(db_name, os.path.join("Data", f"table_queries_{db_name}.sql")):
                if self.ask_for_dummy_data(db_name):
                    self.add_dummy_data(db_name, os.path.join("Data", f'Dummy_Data_{db_name}.sql'))

    def create_all(self):
        self.create_cash_register()
        self.create_vending()
        self.create_users()
        self.create_restaurant()


    def check_database_exists(self, db_name):
        try:
            conn = pymysql.connect(host=Hname, user=Uname, password=Pword)
            cursor = conn.cursor()
            cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
            return cursor.fetchone() is not None
        except pymysql.Error as e:
            print(f"Error checking database existence: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def backup_cash_register(self):
        self.backup_database(db_nameCR)

    def backup_vending(self):
        self.backup_database(db_nameVD)

    def backup_restaurant(self):
        self.backup_database(db_nameRS, ignore_tables=["order", "table"])

    def backup_users(self):
        self.backup_database(db_nameUS)

    def backup_all(self):
        self.backup_cash_register()
        self.backup_vending()
        self.backup_restaurant()
        self.backup_users()

    def backup_database(self, db_name, ignore_tables=None):
        conn = None
        try:
            conn = pymysql.connect(host=Hname, user=Uname, password=Pword, database=db_name)
            cursor = conn.cursor()

            # Fetch table names
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            backup_folder = os.path.join("Backup", db_name)
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)

            # Get current date and time
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Construct backup file name with date
            backup_file_name = f"_backup_{db_name}_{current_date}.sql"

            with open(os.path.join(backup_folder, backup_file_name), "w") as backup_file:
                # Fetch and write data for each table
                for table in tables:
                    table_name = table[0]
                    if ignore_tables and table_name.lower() in ignore_tables:
                        continue
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    # Generate INSERT statements for each row
                    for row in rows:
                        columns = ', '.join([f"`{column[0]}`" for column in cursor.description])
                        values = ', '.join([f"'{conn.escape_string(str(data))}'" if data is not None else 'NULL' for data in row])
                        backup_file.write(f"INSERT INTO `{table_name}` ({columns}) VALUES ({values});\n")

            QMessageBox.information(self, "Backup Success", f"Backup created for '{db_name}' database.")
        except pymysql.Error as e:
            error_message = f"Error creating backup for '{db_name}': {e}"
            QMessageBox.critical(self, "Error", error_message)
        finally:
            if conn:
                conn.close()

    def restore_cash_register(self):
        print("Restore Cash Register button clicked.")
        self.restore_backup.restore_backup(db_nameUS)

    def restore_vending(self):
        print("Restore Vending button clicked.")
        self.restore_backup.restore_backup(db_nameVD)

    def restore_restaurant(self):
        print("Restore Restaurant button clicked.")
        self.restore_backup.restore_backup(db_nameRS)

    def restore_users(self):
        print("Restore Users button clicked.")
        self.restore_backup.restore_backup(db_nameUS)

    def restore_all(self):
        print("Restore All button clicked.")
        self.restore_backup.restore_backup(db_nameCR)
        self.restore_backup.restore_backup(db_nameVD)
        self.restore_backup.restore_backup(db_nameRS)
        self.restore_backup.restore_users(db_nameUS)

    def drop_tables(self):
        dialog = DropTablesDialog(self)
        if dialog.exec() == QDialog.Accepted:
            conn = None
            try:
                # Connect to MySQL without specifying a database
                conn = pymysql.connect(
                    host=Hname,
                    user=Uname,
                    password=Pword
                )

                # Create a cursor object to execute SQL queries
                cursor = conn.cursor()

                # Get a list of databases
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()

                # Exclude system databases
                databases = [db[0] for db in databases if
                             db[0] not in ("information_schema", "mysql", "performance_schema", "sys")]

                # Drop all user-created databases
                for db_name in databases:
                    cursor.execute(f"DROP DATABASE {db_name}")
                    message = f"Database '{db_name}' dropped successfully."
                    self.show_success_message(message)

                self.show_success_message("All user-created databases dropped successfully.")

            except pymysql.Error as e:
                error_message = f"Error dropping databases: {e}"
                QMessageBox.critical(None, "Error", error_message)
            finally:
                if conn:
                    conn.close()

    def show_success_message(self, message):
        msg_box = QMessageBox()
        msg_box.setStyleSheet("background-color: #333333; color: white;")
        msg_box.setWindowTitle("Success")
        msg_box.setText(message)
        msg_box.exec()

    def panic(self):
        try:
            subprocess.Popen(["python", r"Frogger.py"])
        except FileNotFoundError:
            print("Unable to find Frogger.")

    def dbmanager(self):
        try:
            subprocess.Popen(["python", r"DBManager.py"])
        except FileNotFoundError:
            print("Unable to find DBManager.py.")

if __name__ == "__main__":
    app = QApplication([])
    window = ManagementDashboard()
    window.show()
    app.exec()
