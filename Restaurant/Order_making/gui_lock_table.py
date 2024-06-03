from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
import os

ICON_FOLDER = "../Icons/"
class LockTheTable(QDialog):
    about_to_close = Signal()

    def __init__(self, db_connection, table_number, status):
        super().__init__()
        self.db_connection = db_connection
        self.table_number = table_number
        self.status = status
        self.initUI(status)
        self.lock_table()

    def initUI(self, status):
        self.setWindowTitle("Lock Table")
        self.setGeometry(100, 100, 300, 200)
        icon_path = os.path.join(ICON_FOLDER, "favicon.png")
        self.setWindowIcon(QIcon(icon_path))

    def lock_table(self):
        print(f"Locking table {self.table_number}")
        try:
            # Lock the table in the database
            with self.db_connection.cursor() as cursor:
                sql = "UPDATE `tables` SET `rs_status` = 'locked' WHERE `rs_number` = %s"
                cursor.execute(sql, (self.table_number,))
                self.db_connection.commit()
                print(f"Table {self.table_number} locked")
            self.close()
            self.about_to_close.emit()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error locking table: {e}")
            print(e)
            self.close()

class UnlockTheTable(QDialog):
    about_to_close = Signal()

    def __init__(self, db_connection, table_number, status):
        super().__init__()
        self.db_connection = db_connection
        self.table_number = table_number
        self.status = status
        self.initUI(status)
        self.unlock_table()

    def initUI(self, status):
        self.setWindowTitle("Unlock Table")
        self.setGeometry(100, 100, 300, 200)

    def unlock_table(self):
        if self.status == 'locked':
            try:
                # Unlock the table in the database
                with self.db_connection.cursor() as cursor:
                    sql = "UPDATE `tables` SET `rs_status` = 'available' WHERE `rs_number` = %s"
                    cursor.execute(sql, (self.table_number,))
                    self.db_connection.commit()
                    print(f"Table {self.table_number} unlocked")
                self.close()
                self.about_to_close.emit()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error unlocking table: {e}")
                print(e)
                self.close()
