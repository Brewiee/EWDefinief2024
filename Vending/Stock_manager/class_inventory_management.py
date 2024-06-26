# Import necessary modules and classes
from Vending.Database_connector.class_database_connector import database_connector
from Vending.Log_creator.class_custom_logger import CustomLogger
import pymysql


# Define the stock_manager class to manage inventory and vending machines
class stock_manager:
    def __init__(self):
        # Initialize database connector and logger
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        self.logger = CustomLogger("Vending", "Logging")
        # Log messages for debugging, information, and errors
        self.logger.log_debug("Start Stock Manager Debug Log")
        self.logger.log_info("Start Stock Manager Info Log")
        self.logger.log_error("Start Stock Manager Error Log")

    def choose_vending_machine(self):
        # Method to retrieve distinct vending machines and their locations
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT DISTINCT i.vd_inventory_vending_machine_id,
                        v.vd_vending_machine_location
                    FROM vending_machine v
                    INNER JOIN inventory i ON v.vd_vending_machine_ID = i.vd_inventory_vending_machine_id;;
                """
                cursor.execute(sql)
                vending_machine = cursor.fetchall()
                vending_machine_data = []
                if vending_machine:
                    for machine in vending_machine:
                        inventory_id = machine["vd_inventory_vending_machine_id"]
                        vending_location = machine["vd_vending_machine_location"]
                        vending_machine_data.append((inventory_id, vending_location))
                return vending_machine_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error reading vending machines: {e}")
            return None

    def read_inventory(self, vending_machine_id=None):
        # Method to read inventory data, optionally for a specific vending machine
        try:
            with self.connection.cursor() as cursor:
                if vending_machine_id is None:
                    sql = """
                        SELECT i.vd_inventory_id, 
                               p.vd_product_name,
                               i.vd_inventory_stock_quantity,
                               i.vd_inventory_refill_stock,
                               i.vd_inventory_max_stock,
                               i.vd_inventory_min_stock
                        FROM inventory i
                        INNER JOIN product p ON i.vd_inventory_product_id = p.vd_product_id
                    """
                    cursor.execute(sql)
                else:
                    sql = """
                        SELECT i1.vd_inventory_id, 
                               p.vd_product_name,
                               i1.vd_inventory_stock_quantity,
                               i1.vd_inventory_refill_stock,
                               i1.vd_inventory_max_stock,
                               i1.vd_inventory_min_stock
                        FROM inventory i1
                        INNER JOIN product p ON i1.vd_inventory_product_id = p.vd_product_id
                        WHERE i1.vd_inventory_vending_machine_id = %s
                    """
                    cursor.execute(sql, (vending_machine_id,))

                inventory = cursor.fetchall()
                inventory_data = []
                if inventory:
                    for stock in inventory:
                        inventory_id = stock['vd_inventory_id']
                        product_name = stock['vd_product_name']
                        inventory_stock_quantity = stock['vd_inventory_stock_quantity']
                        inventory_refill_stock = stock['vd_inventory_refill_stock']
                        inventory_max_stock = stock['vd_inventory_max_stock']
                        inventory_min_stock = stock['vd_inventory_min_stock']
                        inventory_data.append((
                            inventory_id, product_name, inventory_stock_quantity, inventory_refill_stock,
                            inventory_max_stock, inventory_min_stock))
                return inventory_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error reading products: {e}")
            return None

    def update_stock_quantity(self, inventory_id, inventory_stock_quantity):
        # Method to update the stock quantity of a specific inventory item
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_stock_quantity=%s WHERE vd_inventory_id=%s"
                cursor.execute(sql, (inventory_stock_quantity, inventory_id))
                self.connection.commit()
                self.logger.log_info(f"Stock updated: id: {inventory_id}, stock quantity: {inventory_stock_quantity}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating stock quantity: {e}")
            return False

    def set_refill_stock(self, inventory_product_id, inventory_refill_stock):
        # Method to update the refill stock value for a specific product
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_refill_stock=%s WHERE vd_inventory_product_id=%s"
                cursor.execute(sql, (inventory_refill_stock, inventory_product_id))
                self.connection.commit()
                self.logger.log_info(
                    f"Refill stock updated: id: {inventory_product_id}, refill stock: {inventory_refill_stock}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating refill stock: {e}")
            return False

    def set_max_stock(self, inventory_product_id, inventory_max_stock):
        # Method to update the maximum stock value for a specific product
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_max_stock=%s WHERE vd_inventory_product_id=%s"
                cursor.execute(sql, (inventory_max_stock, inventory_product_id))
                self.connection.commit()
                self.logger.log_info(f"Max stock updated: id: {inventory_product_id}, max stock: {inventory_max_stock}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating max stock: {e}")
            return False

    def set_min_stock(self, inventory_product_id, inventory_min_stock):
        # Method to update the minimum stock value for a specific product
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_min_stock=%s WHERE vd_inventory_product_id=%s"
                cursor.execute(sql, (inventory_min_stock, inventory_product_id))
                self.connection.commit()
                self.logger.log_info(f"Min stock updated: id {inventory_product_id}, min stock: {inventory_min_stock}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating min stock: {e}")
            return False

    def set_stock_to_refill(self, vending_machine_id):
        # Method to set the stock quantity to refill stock for all items in a specific vending machine
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_stock_quantity = vd_inventory_refill_stock WHERE vd_inventory_vending_machine_id = %s"
                cursor.execute(sql, (vending_machine_id,))
                self.connection.commit()
                self.logger.log_info(f"Stock set to refill values: id: {vending_machine_id}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error setting stock to refill: {e}")
            return False

    def set_stock_to_max(self, vending_machine_id):
        # Method to set the stock quantity to maximum stock for all items in a specific vending machine
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_stock_quantity = vd_inventory_max_stock WHERE vd_inventory_vending_machine_id = %s"
                cursor.execute(sql, (vending_machine_id,))
                self.connection.commit()
                self.logger.log_info(f"Stock set to max values: id: {vending_machine_id}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error setting stock to max: {e}")
            return False

    def show_stock_to_refill(self, vending_machine_id):
        # Method to show the stock that needs to be refilled for a specific vending machine
        try:
            with self.connection.cursor() as cursor:
                refill_stock_query = """
                        SELECT i.vd_inventory_product_id,
                               p.vd_product_name, 
                               i.vd_inventory_stock_quantity,
                               i.vd_inventory_refill_stock - i.vd_inventory_stock_quantity AS refill_stock,
                               i.vd_inventory_refill_stock
                        FROM inventory i
                        INNER JOIN product p ON i.vd_inventory_product_id = p.vd_product_id
                        INNER JOIN vending_machine v ON i.vd_inventory_vending_machine_id = v.vd_vending_machine_id
                        WHERE v.vd_vending_machine_id = %s
                        GROUP BY i.vd_inventory_product_id, p.vd_product_name, i.vd_inventory_stock_quantity, i.vd_inventory_refill_stock
                    """
                cursor.execute(refill_stock_query, (vending_machine_id,))
                inventory = cursor.fetchall()
                inventory_refill_data = []
                if inventory:
                    for stock in inventory:
                        inventory_product_id = stock["vd_inventory_product_id"]
                        product_name = stock["vd_product_name"]
                        current_stock = stock["vd_inventory_stock_quantity"]
                        to_refill_stock = stock["refill_stock"]
                        refill_stock = stock["vd_inventory_refill_stock"]
                        inventory_refill_data.append(
                            (inventory_product_id, product_name, current_stock, to_refill_stock, refill_stock))
                return inventory_refill_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error connecting: {e}")

    def show_stock_to_max(self, vending_machine_id):
        # Method to show the stock that needs to be filled to maximum for a specific vending machine
        try:
            with self.connection.cursor() as cursor:
                refill_stock_query = """
                        SELECT i.vd_inventory_product_id,
                               p.vd_product_name, 
                               i.vd_inventory_stock_quantity,
                               i.vd_inventory_max_stock - i.vd_inventory_stock_quantity AS refill_stock,
                               i.vd_inventory_max_stock
                        FROM inventory i
                        INNER JOIN product p ON i.vd_inventory_product_id = p.vd_product_id
                        INNER JOIN vending_machine v ON i.vd_inventory_vending_machine_id = v.vd_vending_machine_id
                        WHERE v.vd_vending_machine_id = %s
                        GROUP BY i.vd_inventory_product_id, p.vd_product_name, i.vd_inventory_stock_quantity, i.vd_inventory_max_stock
                    """
                cursor.execute(refill_stock_query, (vending_machine_id,))
                inventory = cursor.fetchall()
                inventory_refill_data = []
                if inventory:
                    for stock in inventory:
                        inventory_product_id = stock["vd_inventory_product_id"]
                        product_name = stock["vd_product_name"]
                        current_stock = stock["vd_inventory_stock_quantity"]
                        to_refill_stock = stock["refill_stock"]
                        max_stock = stock["vd_inventory_max_stock"]
                        inventory_refill_data.append(
                            (inventory_product_id, product_name, current_stock, to_refill_stock, max_stock))
                return inventory_refill_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error connecting: {e}")

    def update_inventory(self, inventory_id, edited_data):
        # Method to update multiple inventory fields for a specific inventory item
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    UPDATE inventory
                    SET vd_inventory_stock_quantity = %s,
                        vd_inventory_refill_stock = %s,
                        vd_inventory_max_stock = %s,
                        vd_inventory_min_stock = %s
                    WHERE vd_inventory_id = %s
                """
                cursor.execute(sql, (*edited_data, inventory_id))
                self.connection.commit()
                self.logger.log_info(f"Inventory edited: id: {inventory_id}, data: {edited_data}")
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating inventory: {e}")
