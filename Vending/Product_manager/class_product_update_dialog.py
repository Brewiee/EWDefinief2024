from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class ProductUpdateDialog(QDialog):
    """Dialog for updating product information."""

    def __init__(self, current_name, current_price, current_tax, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Product")

        layout = QVBoxLayout()

        self.name_label = QLabel("Product Name:")
        layout.addWidget(self.name_label)
        self.name_entry = QLineEdit(current_name)
        layout.addWidget(self.name_entry)

        self.price_label = QLabel("Product Price:")
        layout.addWidget(self.price_label)
        self.price_entry = QLineEdit(str(current_price))
        layout.addWidget(self.price_entry)

        self.tax_label = QLabel("Product Tax:")
        layout.addWidget(self.tax_label)
        self.tax_entry = QLineEdit(str(current_tax))
        layout.addWidget(self.tax_entry)

        self.update_button = QPushButton("Update Product")
        self.update_button.clicked.connect(self.accept)
        layout.addWidget(self.update_button)

        self.setLayout(layout)

    def get_updated_info(self):
        """Get updated product information."""
        new_name = self.name_entry.text()
        new_price = float(self.price_entry.text())
        new_tax = float(self.tax_entry.text())
        return new_name, new_price, new_tax