from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide6.QtCore import Signal
import pymysql

class AddPostalCodeDialog(QDialog):
    # Define a signal to emit postal code and city
    postal_code_saved = Signal(str, str)

    def __init__(self, postal_code):
        super().__init__()
        self.setWindowTitle("Add New Postal Code")
        self.postal_code = postal_code  # Store the postal code
        layout = QVBoxLayout()

        self.postal_code_label = QLabel("Postal Code:")
        self.postal_code_input = QLineEdit()
        self.postal_code_input.setText(postal_code)  # Pre-fill the postal code
        self.postal_code_input.setReadOnly(True)  # Make the postal code field read-only
        layout.addWidget(self.postal_code_label)
        layout.addWidget(self.postal_code_input)

        self.city_label = QLabel("City:")
        self.city_input = QLineEdit()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_postal_code)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_postal_code(self):
        postal_code = self.postal_code_input.text()
        city = self.city_input.text()

        # Save the postal code to the database
        try:
            with self.conn.cursor() as cursor:
                query = "INSERT INTO postalcode (CR_PostalCode_Zipcode, CR_PostalCode_City) VALUES (%s, %s)"
                cursor.execute(query, (postal_code, city))
                self.conn.commit()

            QMessageBox.information(self, "Success", "Postal code saved successfully.")
            self.accept()  # Close the dialog window after saving

            # Emit the signal with postal code and city
            self.postal_code_saved.emit(postal_code, city)
        except pymysql.Error as e:
            QMessageBox.warning(self, "Error", f"Error saving postal code: {str(e)}")
