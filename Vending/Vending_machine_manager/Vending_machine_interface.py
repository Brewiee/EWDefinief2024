from Vending.Log_creator.class_custom_logger import CustomLogger
from Vending.Database_connector.class_database_connector import database_connector
import pymysql

class vending_machine_interface:
    def __init__(self):
        self.logger = CustomLogger("Vending", "Logging")
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        self.logger.log_debug("Start Vending Machine Interface Debug Log")
        self.logger.log_info("Start Vending Machine Info Log")
        self.logger.log_error("Start Vending Machine Error Log")

    def create_vending_machine(self, vending_location, vending_address, vending_postal_code, vending_city,
                               vending_country):
        try:
            with self.connection.cursor() as cursor:
                sql = ("INSERT INTO vending_machine (vd_vending_machine_location, vd_vending_machine_address, vd_vending_machine_postal_code, "
                       "vd_vending_machine_city, vd_vending_machine_country) VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(sql, (vending_location, vending_address, vending_postal_code, vending_city, vending_country))
                self.connection.commit()
                self.logger.log_info(
                    f"Machine created: (Vending location:{vending_location}), (Vending address: {vending_address}), (Vending postal code: {vending_postal_code}), (Vending city: {vending_city}), (Vending country: {vending_country}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error creating vending machine: {e}")
            return False
        finally:
            self.logger.log_info("Vending machine creation process completed.")

    def update_vending_machine(self, vending_id, vending_location, vending_address, vending_postal_code, vending_city,
                               vending_country):
        self.logger.log_debug(
            f"Updating Vending ID: {vending_id}, Vending Location: {vending_location}, Vending Address: {vending_address}, Postal Code: {vending_postal_code}, City: {vending_city}, Country: {vending_country}")
        try:
            with self.connection.cursor() as cursor:
                sql = ("UPDATE vending_machine SET vd_vending_machine_location=%s, vd_vending_machine_address=%s, vd_vending_machine_postal_code=%s, "
                       "vd_vending_machine_city=%s, vd_vending_machine_country=%s WHERE vd_vending_machine_id=%s")
                cursor.execute(sql, (vending_location, vending_address, vending_postal_code, vending_city, vending_country, vending_id))
                self.connection.commit()
                self.logger.log_debug(
                    f"Machine updated:(Vending ID: {vending_id} ,(Vending location:{vending_location}), (Vending address: {vending_address}), "
                    f"(Vending postal code: {vending_postal_code}), (Vending city: {vending_city}), (Vending country: {vending_country}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating product: {e}")
            return False
        finally:
            self.logger.log_info("Vending machine update process completed.")

    def delete_vending_machine(self, vending_id):
        try:
            with self.connection.cursor() as cursor:
                # First, attempt to delete associated records in the inventory table
                sql_delete_inventory = "DELETE FROM inventory WHERE vd_inventory_vending_machine_id=%s"
                cursor.execute(sql_delete_inventory, (vending_id,))
                # Next, attempt to delete the vending machine
                sql_delete_vending_machine = "DELETE FROM vending_machine WHERE vd_vending_machine_id=%s"
                cursor.execute(sql_delete_vending_machine, (vending_id,))
                self.connection.commit()
                self.logger.log_info(f"vending id: {vending_id} deleted")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error deleting vending machine: {e}")
            return False

    def read_products(self):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM product"
                cursor.execute(sql)
                products = cursor.fetchall()
                product_data = []
                if products:
                    for product in products:
                        product_id = product['vd_product_id']
                        product_name = product['vd_product_name']
                        product_data.append((product_id, product_name))
                return product_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error reading products: {e}")
            return None

    def choose_vending_machine(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT DISTINCT v.vd_vending_machine_id,
                        v.vd_vending_machine_location
                    FROM vending_machine v
                """
                cursor.execute(sql)
                vending_machine = cursor.fetchall()
                vending_machine_data = []
                if vending_machine:
                    for machine in vending_machine:
                        inventory_id = machine["vd_vending_machine_id"]
                        vending_location = machine["vd_vending_machine_location"]
                        vending_machine_data.append((inventory_id, vending_location))  # Use [] to append as a tuple
                return vending_machine_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error reading vending machines: {e}")
            return None

    def get_vending_machine_data(self, machine_name):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM vending_machine WHERE vd_vending_machine_location = %s"
                cursor.execute(sql, (machine_name,))
                machine_data = cursor.fetchone()
                return machine_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error getting machine data: {e}")
            return None

    def set_up_vending_machine(self, vending_machine_id, product_id, min_stock=0, max_stock=0, refill_stock=0):
        try:
            with self.connection.cursor() as cursor:
                # Check if the product already exists in the inventory for the vending machine
                sql_check = """
                        SELECT vd_inventory_vending_machine_id FROM inventory 
                        WHERE vd_inventory_product_id = %s AND vd_inventory_vending_machine_id = %s
                    """
                cursor.execute(sql_check, (product_id, vending_machine_id))
                result = cursor.fetchone()

                if result:
                    self.logger.log_debug(f"Product {product_id} already exists in the inventory for this vending machine.")
                    return False
                else:
                    # Insert the product into the inventory table for the vending machine
                    sql_insert = """
                            INSERT INTO inventory (vd_inventory_vending_machine_id, vd_inventory_product_id, vd_inventory_stock_quantity, vd_inventory_min_stock, vd_inventory_max_stock, vd_inventory_refill_stock) 
                            VALUES (%s, %s, 0, %s, %s, %s)
                        """
                    cursor.execute(sql_insert, (vending_machine_id, product_id, min_stock, max_stock, refill_stock))
                    self.connection.commit()
                    self.logger.log_info(f"Product {product_id} added to inventory for the vending machine.")
                    return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error setting up vending machine: {e}")
            return False