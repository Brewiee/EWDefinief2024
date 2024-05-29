from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, \
    QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QLineEdit, QSpacerItem, QMenu, QFileDialog, QDialog, QFormLayout
from PySide6.QtGui import QAction
from stylesheet_prog_database_manager import databasemanagerstylesheet
import pymysql
import csv
import codecs
from xlsxwriter.workbook import Workbook
from fpdf import FPDF
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox
import pandas as pd
from datetime import datetime
import os


class DatabaseManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Manager")
        self.setGeometry(0,0,1900,1000)

        # Connect to the database
        self.conn = self.connect_to_database()

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)


        # Selector widget
        self.selector_widget = QWidget()
        selector_layout = QHBoxLayout(self.selector_widget)
        self.layout.addWidget(self.selector_widget)

        self.selector_label = QLabel("Select:")
        selector_layout.addWidget(self.selector_label)
        self.selector_label.setStyleSheet(databasemanagerstylesheet.label())

        self.table_combo = QComboBox()
        selector_layout.addWidget(self.table_combo)
        self.table_combo.setStyleSheet(databasemanagerstylesheet.combo_box())


        self.database_label = QLabel("from database:")
        selector_layout.addWidget(self.database_label)
        self.database_label.setStyleSheet(databasemanagerstylesheet.label())

        self.database_combo = QComboBox()
        selector_layout.addWidget(self.database_combo)
        self.database_combo.setStyleSheet(databasemanagerstylesheet.combo_box())

        # Search table widget
        self.search_table_widget = QWidget()
        search_layout = QHBoxLayout(self.search_table_widget)
        self.layout.addWidget(self.search_table_widget)


        self.search_label = QLabel("Search table for:")
        search_layout.addWidget(self.search_label)
        self.search_edit = QLineEdit()
        search_layout.addWidget(self.search_edit)

        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.table_widget)
        self.table_widget.setStyleSheet(databasemanagerstylesheet.table_widget())

        # Button widget
        self.button_widget = QWidget()
        button_layout = QVBoxLayout(self.button_widget)
        self.layout.addWidget(self.button_widget)

        self.button1 = QPushButton("Import witch .csv")
        button_layout.addWidget(self.button1)
        self.button1.clicked.connect(self.import_csv)
        self.button1.setStyleSheet(databasemanagerstylesheet.pushbutton())

        self.button2 = QPushButton("Selected data extractor")
        button_layout.addWidget(self.button2)
        self.button2.setMenu(self.create_export_menu())
        self.button2.setStyleSheet(databasemanagerstylesheet.pushbutton())


        # After creating the button_widget, clear the layout and recreate it with the buttons in a QVBoxLayout
        self.button_widget = QWidget()
        button_layout = QVBoxLayout(self.button_widget)

        self.update_selected_button = QPushButton("Update Selected Rows")
        self.update_selected_button.clicked.connect(self.update_selected_rows)
        button_layout.addWidget(self.update_selected_button)
        self.update_selected_button.setStyleSheet(databasemanagerstylesheet.pushbutton())

        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        button_layout.addWidget(self.add_row_button)
        self.add_row_button.setStyleSheet(databasemanagerstylesheet.pushbutton())

        self.delete_selected_button = QPushButton("Delete Selected Rows")
        self.delete_selected_button.clicked.connect(self.delete_selected_rows)
        button_layout.addWidget(self.delete_selected_button)
        self.delete_selected_button.setStyleSheet(databasemanagerstylesheet.pushbutton())

        self.clear_table_button = QPushButton("Clear All Table Values")
        self.clear_table_button.clicked.connect(self.clear_all_table_values)
        button_layout.addWidget(self.clear_table_button)
        self.clear_table_button.setStyleSheet(databasemanagerstylesheet.pushbutton())

        # Add the button container widget to the main layout, aligned to the right side
        self.layout.addWidget(self.button_widget, alignment=Qt.AlignTop | Qt.AlignRight)

        # Initialize UI
        self.init_ui()

    def apply_stylesheet(self):
        # Apply stylesheet to each widget
        self.setStyleSheet(databasemanagerstylesheet.central_widget())
        self.selector_label.setStyleSheet(databasemanagerstylesheet.label())

        self.search_label.setStyleSheet(databasemanagerstylesheet.label())




        self.button2.setStyleSheet(databasemanagerstylesheet.pushbutton())

    def init_ui(self):
        if self.conn:
            # Populate the database combo box with available databases
            databases = self.get_database_list()
            self.database_combo.addItem("First: Select database")
            self.database_combo.addItems(databases)
            self.database_combo.currentIndexChanged.connect(self.populate_table_combo)
            self.populate_table_combo(0)
        else:
            QMessageBox.warning(self, "Error", "Failed to connect to the database.")

        # Connect the textChanged signal of the search edit to a slot
        self.search_edit.textChanged.connect(self.filter_table_data)

        # Connect the header clicked signal to show the context menu
        self.table_widget.horizontalHeader().sectionClicked.connect(self.show_context_menu)

    def connect_to_database(self):
        try:
            conn = pymysql.connect(
                host="localhost",
                user="dbadmin",
                password="dbadmin",
            )
            return conn
        except pymysql.Error as err:
            print("Error:", err)
            return None

    def get_database_list(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute("SHOW DATABASES")
                databases = [row[0] for row in cursor.fetchall()]
                return databases
            except pymysql.Error as err:
                print("Error:", err)
        return []

    def populate_table_combo(self, index):
        self.table_combo.clear()
        if index > 0:
            selected_database = self.database_combo.currentText()
            if self.conn and selected_database != "First: Select database":
                try:
                    cursor = self.conn.cursor()
                    cursor.execute(f"USE {selected_database}")
                    cursor.execute("SHOW TABLES")
                    tables = [row[0] for row in cursor.fetchall()]
                    self.table_combo.addItem("Select table")
                    self.table_combo.addItems(tables)
                    self.table_combo.currentIndexChanged.connect(self.populate_table_data)
                except pymysql.Error as err:
                    print("Error:", err)
            else:
                QMessageBox.warning(self, "Error", "Please select a valid database.")


    def populate_table_data(self, index):
        self.table_widget.clear()
        if index > 0:
            selected_table = self.table_combo.currentText()
            if selected_table != "Select table":
                try:
                    cursor = self.conn.cursor()
                    cursor.execute(f"SELECT * FROM {selected_table}")
                    rows = cursor.fetchall()
                    num_rows = len(rows)
                    num_columns = len(cursor.description)
                    self.table_widget.setRowCount(num_rows)
                    self.table_widget.setColumnCount(num_columns)
                    column_names = [description[0] for description in cursor.description]
                    self.table_widget.setHorizontalHeaderLabels(column_names)
                    for i, row in enumerate(rows):
                        for j, value in enumerate(row):
                            item = QTableWidgetItem(str(value))
                            self.table_widget.setItem(i, j, item)
                except pymysql.Error as err:
                    print("Error:", err)
                    return
    def filter_table_data(self, text):
        if text:
            text = text.lower()
            for row in range(self.table_widget.rowCount()):
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item:
                        if text in item.text().lower():
                            self.table_widget.setRowHidden(row, False)
                            break
                else:
                    self.table_widget.setRowHidden(row, True)
        else:
            for row in range(self.table_widget.rowCount()):
                self.table_widget.setRowHidden(row, False)

    def show_context_menu(self, index):
        menu = QMenu(self)
        sort_a_to_z_action = menu.addAction("Sort A to Z")
        sort_z_to_a_action = menu.addAction("Sort Z to A")
        action = menu.exec_(self.table_widget.mapToGlobal(index))

        if action == sort_a_to_z_action:
            self.sort_column(index, Qt.AscendingOrder)
        elif action == sort_z_to_a_action:
            self.sort_column(index, Qt.DescendingOrder)

    def sort_column(self, column, order):
        self.table_widget.sortItems(column, order)

    def create_export_menu(self):
        menu = QMenu(self)
        csv_action = QAction("Export to CSV", self)
        pdf_action = QAction("Export to PDF", self)
        excel_action = QAction("Export to Excel", self)
        sql_query_action = QAction("Generate SQL Query", self)
        import_template_action = QAction("Create Import Template", self)

        csv_action.triggered.connect(lambda: self.export_data("csv"))
        pdf_action.triggered.connect(lambda: self.export_data("pdf"))
        excel_action.triggered.connect(lambda: self.export_data("excel"))
        sql_query_action.triggered.connect(self.generate_sql_query)
        import_template_action.triggered.connect(self.create_import_template)

        menu.addAction(csv_action)
        menu.addAction(pdf_action)
        menu.addAction(excel_action)
        menu.addAction(sql_query_action)
        menu.addAction(import_template_action)

        return menu

    def create_import_template(self):
        selected_database = self.database_combo.currentText()
        selected_table = self.table_combo.currentText()
        if selected_database == "First: Select database" or selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid database and table.")
            return

        file_name = f"{selected_database}_{selected_table}_importtemplate.xlsx"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Import Template", file_name, "Excel Files (*.xlsx)")
        if file_path:
            workbook = Workbook(file_path)
            worksheet = workbook.add_worksheet()
            # Write column headers
            headers = [self.table_widget.horizontalHeaderItem(col).text() for col in
                       range(self.table_widget.columnCount())]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            workbook.close()

    def import_csv(self):
        selected_table = self.table_combo.currentText()
        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                # Read CSV file
                with codecs.open(file_path, 'r', encoding='utf-8-sig') as csvfile:
                    dialect = csv.Sniffer().sniff(csvfile.read(1024))
                    csvfile.seek(0)
                    reader = csv.reader(csvfile, dialect)

                    # Read the header row to get the column names
                    csv_headers = next(reader)

                    # Prompt the user with a dialog box to ask how to handle duplicates
                    dup_dialog = QMessageBox(self)
                    dup_dialog.setWindowTitle("Duplicate Values")
                    dup_dialog.setText("How do you want to handle duplicate values?")
                    dup_dialog.setStandardButtons(QMessageBox.NoButton)  # No standard buttons
                    overwrite_button = dup_dialog.addButton("Overwrite", QMessageBox.ActionRole)
                    skip_button = dup_dialog.addButton("Skip", QMessageBox.ActionRole)

                    # Execute the dialog and handle user response
                    dup_result = dup_dialog.exec()

                    # Check which button was clicked and assign the appropriate action
                    if dup_dialog.clickedButton() == overwrite_button:
                        handle_duplicates = "overwrite"
                    else:
                        handle_duplicates = "skip"

                    print("Handling duplicates:", handle_duplicates)

                    # Read CSV file and handle headers accordingly
                    placeholders = ", ".join(["%s"] * len(csv_headers))
                    query = f"INSERT INTO {selected_table} ({', '.join(csv_headers)}) VALUES ({placeholders})"
                    cursor = self.conn.cursor()

                    try:
                        for row in reader:
                            # Check if the row exists in the table
                            select_query = f"SELECT * FROM {selected_table} WHERE {csv_headers[0]} = %s"
                            cursor.execute(select_query, (row[0],))
                            existing_row = cursor.fetchone()

                            if existing_row:
                                # Handle duplicate values according to the chosen strategy
                                if handle_duplicates == "overwrite":
                                    # Update the existing row
                                    update_query = f"UPDATE {selected_table} SET "
                                    update_query += ", ".join([f"{col} = %s" for col in csv_headers])
                                    update_query += f" WHERE {csv_headers[0]} = %s"
                                    cursor.execute(update_query, (*row, row[0]))
                            else:
                                # Insert a new row
                                cursor.execute(query, row)

                        # Commit changes after processing all rows
                        self.conn.commit()

                        # Update the table view with the new data
                        self.populate_table_data(self.table_combo.currentIndex())

                    finally:
                        csvfile.close()  # Close the file after reading


            except Exception as e:
                # Display an error message box with a "Copy Error" button
                error_dialog = QMessageBox(self)
                error_dialog.setWindowTitle("Error")
                error_dialog.setText(f"Failed to import data: {str(e)}")
                error_dialog.setIcon(QMessageBox.Critical)
                copy_button = QPushButton("Copy Error")
                copy_button.clicked.connect(lambda: self.copy_to_clipboard(str(e)))
                layout = QVBoxLayout()
                layout.addWidget(copy_button)
                error_dialog.setLayout(layout)
                error_dialog.exec()



    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
    def export_data(self, export_format):
        selected_table = self.table_combo.currentText()
        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return

        selected_rows = self.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "No rows selected for export.")
            return

        if export_format == "csv":
            self.export_to_csv(selected_rows)
        elif export_format == "pdf":
            self.export_to_pdf(selected_rows)
        elif export_format == "excel":
            self.export_to_excel(selected_rows)

    def get_selected_rows(self):
        if self.search_edit.text():
            return self.get_search_results()
        else:
            return self.get_all_rows()

    def get_search_results(self):
        search_text = self.search_edit.text().lower()
        selected_rows = []
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item and search_text in item.text().lower():
                    selected_rows.append(item)
                    break
        return selected_rows

    def get_all_rows(self):
        all_rows = []
        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    all_rows.append(item)
        return all_rows

    def export_to_csv(self, selected_rows):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write column headers
                headers = [self.table_widget.horizontalHeaderItem(col).text() for col in
                           range(self.table_widget.columnCount())]
                writer.writerow(headers)
                # Write data
                for row in range(self.table_widget.rowCount()):
                    row_data = []
                    for col in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(row, col)
                        if item:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    writer.writerow(row_data)

    def export_to_pdf(self, selected_rows):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            # Add column headers
            headers = [self.table_widget.horizontalHeaderItem(col).text() for col in
                       range(self.table_widget.columnCount())]
            pdf.set_fill_color(200, 220, 255)
            for col, header in enumerate(headers):
                pdf.cell(40, 10, header, 1, 0, 'C', 1)
            pdf.ln()

            # Add data
            for row in range(self.table_widget.rowCount()):
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item:
                        pdf.cell(40, 10, item.text(), 1)
                pdf.ln()

            pdf.output(file_path)

    def export_to_excel(self, selected_rows):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel", "", "Excel Files (*.xlsx)")
        if file_path:
            workbook = Workbook(file_path)
            worksheet = workbook.add_worksheet()
            # Write column headers
            headers = [self.table_widget.horizontalHeaderItem(col).text() for col in
                       range(self.table_widget.columnCount())]
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            # Write data
            for row in range(self.table_widget.rowCount()):
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item:
                        worksheet.write(row + 1, col, item.text())
                    else:
                        worksheet.write(row + 1, col, "")
            workbook.close()


    def guess_primary_key(self):
        potential_primary_keys = []

        int_primary_key = None
        leftmost_primary_key = None

        for col in range(self.table_widget.columnCount()):
            column_name = self.table_widget.horizontalHeaderItem(col).text()
            unique_values = set()
            has_null = False
            has_duplicate = False
            is_int_column = True  # Assume the column is integer by default

            for row in range(self.table_widget.rowCount()):
                item = self.table_widget.item(row, col)
                if item:
                    value = item.text()
                    # Check for NULL values
                    if not value:
                        has_null = True
                    # Check for uniqueness
                    elif value in unique_values:
                        has_duplicate = True
                    else:
                        unique_values.add(value)
                    # Check if the value can be converted to an integer
                    if not value.isdigit():
                        is_int_column = False

            # Check if column meets criteria for potential primary key
            if not has_null and not has_duplicate:
                potential_primary_keys.append(column_name)
                # Check if the current column is an integer and update the int_primary_key
                if is_int_column and int_primary_key is None:
                    int_primary_key = column_name
                # Update the leftmost_primary_key
                if leftmost_primary_key is None:
                    leftmost_primary_key = column_name

        # If there are multiple potential primary keys, choose based on the priority
        if len(potential_primary_keys) > 1:
            if int_primary_key:
                return [int_primary_key]  # Return the integer primary key
            else:
                return [leftmost_primary_key]  # Return the leftmost primary key
        else:
            return potential_primary_keys  # Return the single potential primary key

    def generate_sql_query(self):
        selected_table = self.table_combo.currentText()

        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return

        query = f"CREATE TABLE IF NOT EXISTS enter_database_here.{selected_table} (\n"
        column_details = []

        # Guess primary key
        potential_primary_keys = self.guess_primary_key()

        for col in range(self.table_widget.columnCount()):
            column_name = self.table_widget.horizontalHeaderItem(col).text()
            data_type = "VARCHAR(255)"  # Default data type if not specified
            constraints = []

            # Flags to track constraints
            is_auto_increment = False
            is_not_null = False

            # Values set to determine uniqueness
            unique_values = set()

            # Values set to determine auto-increment
            prev_value = None
            is_auto_increment_possible = True

            # Flag to track if 0 value is found
            zero_value_found = False

            # Analyze data in each row of the column
            for row in range(self.table_widget.rowCount()):
                item = self.table_widget.item(row, col)
                if item:
                    # Check for data type based on the item's data role
                    if item.data(Qt.UserRole) is not None:
                        data_type = item.data(Qt.UserRole)
                    # Analyze the value and adjust data type if necessary
                    value = item.text()
                    if value.isdigit():
                        data_type = "INT"  # Change data type to INT for numeric values
                    elif value.lower() in ("true", "false"):
                        data_type = "BOOLEAN"  # Change data type to BOOLEAN for boolean values
                    # Check for constraints
                    if value == "NOT NULL":
                        constraints.append("NOT NULL")
                        is_not_null = True
                    elif value == "PRIMARY KEY":
                        constraints.append("PRIMARY KEY")
                    elif value.startswith("FOREIGN KEY"):
                        constraints.append(value)
                    elif value == "AUTO_INCREMENT":
                        is_auto_increment = True
                    else:
                        unique_values.add(value)  # Add value to the set of unique values

                    # Check for auto-increment condition if data type is INT
                    if data_type == "INT":
                        if prev_value is not None:
                            if not value.isdigit() or int(value) != prev_value + 1:
                                is_auto_increment_possible = False
                        prev_value = int(value) if value.isdigit() else None
                    else:
                        is_auto_increment_possible = False  # Disable auto-increment for non-integer data types

                    # Check for zero value
                    if value == "0":
                        zero_value_found = True

            # Check if all values in the column are unique
            if len(unique_values) == self.table_widget.rowCount():
                constraints.append("UNIQUE")

            # Add auto-increment constraint if applicable
            if is_auto_increment_possible and data_type == "INT":
                constraints.append("AUTO_INCREMENT")

            # Add not null constraint if applicable
            if not zero_value_found:
                constraints.append("NOT NULL")
                is_not_null = True

            # If column is in potential primary keys, add it as primary key constraint
            if column_name in potential_primary_keys:
                constraints.append("PRIMARY KEY")

            # Construct column details
            column_details.append(f"    {column_name} {data_type} {' '.join(constraints)}")

        query += ",\n".join(column_details)
        query += "\n);"

        # Display the generated SQL query in a text box
        text_box = QMessageBox(self)
        text_box.setWindowTitle("Generated SQL Query")
        text_box.setText(query)
        text_box.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

        # Add a button to copy the query to the clipboard
        copy_button = text_box.addButton("Copy to Clipboard", QMessageBox.ActionRole)
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(query))

        text_box.exec()

    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def create_backup(self, data, button_name, database_name, selected_table):
        # Convert list to DataFrame if necessary
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = data

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d-%Hh%M')

        # Specify the directory for backups
        backup_directory = os.path.expanduser(
            r"C:\Users\janha\OneDrive\Documenten\SYNTRA PXL\PYTHON\Eindwerk2024\Jan-Willem\Backups")

        # Create the directory if it doesn't exist
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        # Generate backup file name
        backup_file = os.path.join(backup_directory, f"{database_name}-{selected_table}-{button_name}{timestamp}.csv")

        # Save DataFrame to CSV
        df.to_csv(backup_file, index=False)

        print(f"Backup created: {backup_file}")

    def get_backupvalues(self):
        # Initialize an empty list to store table data
        table_data = []

        # Get column headers
        headers = [self.table_widget.horizontalHeaderItem(col).text() for col in range(self.table_widget.columnCount())]

        # Iterate over rows in the table
        for row in range(self.table_widget.rowCount()):
            row_data = []
            # Iterate over columns in the row
            for col in range(self.table_widget.columnCount()):
                item = self.table_widget.item(row, col)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            table_data.append(row_data)

        # Convert list of lists to DataFrame
        df = pd.DataFrame(table_data, columns=headers)

        return df

    def update_selected_rows(self):

        table_data = self.get_backupvalues()
        cursor = self.conn.cursor()
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        # Retrieve selected table name
        selected_table = self.table_combo.currentText()
        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return
        self.create_backup(table_data, button_name="Row update", database_name=database_name, selected_table=selected_table)

        selected_rows = self.table_widget.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "No rows selected for update.")
            return

        row_index = selected_rows[0].row()  # Assuming only one row can be updated at a time
        selected_column_names = [self.table_widget.horizontalHeaderItem(item.column()).text() for item in selected_rows]
        current_values = [self.table_widget.item(row_index, item.column()).text() for item in selected_rows]

        # Display the values next to the labels
        updated_values = UpdateRowDialog.get_updated_row_data(selected_column_names, current_values)
        if updated_values:
            selected_table = self.table_combo.currentText()
            if selected_table == "Select table":
                QMessageBox.warning(self, "Error", "Please select a valid table.")
                return

            try:
                cursor = self.conn.cursor()
                primary_key_column_name = self.table_widget.horizontalHeaderItem(
                    0).text()  # Assuming the first column is the primary key
                primary_key = self.table_widget.item(row_index, 0).text()
                for col_name, new_value in zip(selected_column_names, updated_values):
                    update_query = f"UPDATE {selected_table} SET {col_name} = %s WHERE {primary_key_column_name} = %s"
                    cursor.execute(update_query, (new_value, primary_key))

                self.conn.commit()  # Move commit operation outside the loop
                self.populate_table_data(self.table_combo.currentIndex())
                QMessageBox.information(self, "Success", "Selected rows updated successfully.")

            except pymysql.Error as err:
                print("Error:", err)
                QMessageBox.critical(self, "Error", f"Failed to update selected rows: {str(err)}")


    def delete_selected_rows(self):

        table_data = self.get_backupvalues()
        cursor = self.conn.cursor()
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        # Retrieve selected table name
        selected_table = self.table_combo.currentText()
        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return
        self.create_backup(table_data, button_name="Delete", database_name=database_name, selected_table=selected_table)

        selected_rows = self.table_widget.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Error", "No rows selected for deletion.")
            return

        # Ask for confirmation
        confirmation = QMessageBox.question(self, "Confirm Deletion",
                                            "Are you sure you want to delete the selected rows?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            selected_primary_keys = set()  # Assuming the primary key is in the first column
            for item in selected_rows:
                row_index = item.row()
                primary_key = self.table_widget.item(row_index, 0).text()
                selected_primary_keys.add(primary_key)

            # Delete the selected rows from the table and the database
            selected_table = self.table_combo.currentText()
            if selected_table == "Select table":
                QMessageBox.warning(self, "Error", "Please select a valid table.")
                return

            try:
                cursor = self.conn.cursor()
                for primary_key in selected_primary_keys:
                    delete_query = f"DELETE FROM {selected_table} WHERE {self.table_widget.horizontalHeaderItem(0).text()} = %s"
                    cursor.execute(delete_query, (primary_key,))
                self.conn.commit()
                QMessageBox.information(self, "Success", "Selected rows deleted successfully.")
                self.populate_table_data(self.table_combo.currentIndex())  # Refresh the table
            except pymysql.Error as err:
                print("Error:", err)
                QMessageBox.critical(self, "Error", f"Failed to delete selected rows: {str(err)}, No changes have been made!")
                self.populate_table_data(self.table_combo.currentIndex())

    def clear_all_table_values(self):

        table_data = self.get_backupvalues()
        cursor = self.conn.cursor()
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        # Retrieve selected table name
        selected_table = self.table_combo.currentText()
        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return
        self.create_backup(table_data, button_name="Clear table", database_name=database_name, selected_table=selected_table)

        # Ask for confirmation
        confirmation = QMessageBox.question(self, "Confirm Clear", "Are you sure you want to clear the table?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            # Clear all values from the table
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)

            # Delete all records from the table in the database
            try:
                cursor = self.conn.cursor()
                delete_query = f"DELETE FROM {selected_table}"
                cursor.execute(delete_query)
                self.populate_table_data(self.table_combo.currentIndex())
                self.conn.commit()
                QMessageBox.information(self, "Success", "All table values cleared successfully.")
            except pymysql.Error as err:
                print("Error:", err)
                QMessageBox.critical(self, "Error", f"Failed to delete selected rows: {str(err)}, No changes have been made")
                self.populate_table_data(self.table_combo.currentIndex())  # Refresh the table

    def add_row(self):
        table_data = self.get_backupvalues()
        cursor = self.conn.cursor()
        cursor.execute("SELECT DATABASE()")
        database_name = cursor.fetchone()[0]

        # Retrieve selected table name
        selected_table = self.table_combo.currentText()
        if selected_table == "Select table":
            QMessageBox.warning(self, "Error", "Please select a valid table.")
            return
        self.create_backup(table_data, button_name="Add row", database_name=database_name, selected_table=selected_table)



        column_names = [self.table_widget.horizontalHeaderItem(col).text() for col in
                        range(self.table_widget.columnCount())]
        new_row_data = AddRowDialog.get_new_row_data(column_names)
        if new_row_data:
            try:
                cursor = self.conn.cursor()
                placeholders = ", ".join(["%s"] * len(new_row_data))
                insert_query = f"INSERT INTO {selected_table} ({', '.join(column_names)}) VALUES ({placeholders})"
                cursor.execute(insert_query, new_row_data)
                self.conn.commit()
                self.populate_table_data(self.table_combo.currentIndex())  # Refresh the table
                QMessageBox.information(self, "Success", "New row added successfully.")
            except pymysql.Error as err:
                print("Error:", err)
                QMessageBox.critical(self, "Error", f"Failed to add new row: {str(err)}")

class AddRowDialog(QDialog):
    def __init__(self, column_names):
        super().__init__()
        self.setWindowTitle("Add New Row")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create labels and input fields for each column
        self.input_fields = []
        for column_name in column_names:
            label = QLabel(column_name)
            input_field = QLineEdit()
            self.input_fields.append(input_field)
            form_layout.addRow(label, input_field)

        layout.addLayout(form_layout)

        # Add buttons
        self.add_button = QPushButton("Add")
        self.cancel_button = QPushButton("Cancel")
        self.add_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.add_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_input_data(self):
        return [field.text() for field in self.input_fields]

    @staticmethod
    def get_new_row_data(column_names):
        dialog = AddRowDialog(column_names)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.get_input_data()
        return None
class UpdateRowDialog(QDialog):
    def __init__(self, column_names, current_values):
        super().__init__()
        self.setWindowTitle("Update Row")

        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create labels and input fields for each column, prefilling with current values
        self.input_fields = []
        for column_name, current_value in zip(column_names, current_values):
            label = QLabel(column_name)
            input_field = QLineEdit()
            input_field.setText(current_value)
            self.input_fields.append(input_field)
            form_layout.addRow(label, input_field)

        layout.addLayout(form_layout)

        # Add buttons
        self.update_button = QPushButton("Update")
        self.cancel_button = QPushButton("Cancel")
        self.update_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.update_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_input_data(self):
        return [field.text() for field in self.input_fields]

    @staticmethod
    def get_updated_row_data(column_names, current_values):
        dialog = UpdateRowDialog(column_names, current_values)
        result = dialog.exec()
        if result == QDialog.Accepted:
            return dialog.get_input_data()
        return None


if __name__ == "__main__":
    app = QApplication([])
    database_manager = DatabaseManager()
    database_manager.show()
    app.exec()
