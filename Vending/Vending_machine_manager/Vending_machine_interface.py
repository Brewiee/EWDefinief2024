from src.Vending_UI.Log_creator.class_custom_logger import CustomLogger
from src.Vending_UI.Database_connector.class_database_connector import database_connector
import pymysql

class vending_machine_interface:
    def __init__(self):
        self.logger = CustomLogger("Vending_creator", "Logging")
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        self.logger.log_debug("Start Vending Creator")

    def run_vending_machine_interface(self):
        while True:
            print("\nVending Creator:")
            print("1. Create machine")
            print("2. Update machine")
            print("3. Delete machine")
            print("4. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                vending_location = input("What is the location of the machine ")
                vending_address = input("Give the address ")
                vending_postal_code = int(input("Postal code "))
                vending_city = input("city ")
                vending_country = input("country ")
                success = self.create_vending_machine(vending_location, vending_address, vending_postal_code, vending_city, vending_country)
                if success:
                    print("Machine created successfully")
            elif choice == "2":
                vending_id = int(input("vending id? "))
                vending_location = input("What is the location of the machine ")
                vending_address = input("Give the address ")
                vending_postal_code = int(input("Postal code "))
                vending_city = input("city ")
                vending_country = input("country ")
                success = self.update_vending_machine(vending_id, vending_location, vending_address, vending_postal_code,
                                                      vending_city, vending_country)
                if success:
                    print("Machine updated successfully")
            elif choice == "3":
                vending_id = int(input("ID to delete? "))
                success = self.delete_vending_machine(vending_id)
                if success:
                    print("Machine deleted successfully")
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_vending_machine(self, vending_location, vending_address, vending_postal_code, vending_city,
                               vending_country):
        try:
            with self.connection.cursor() as cursor:
                sql = ("INSERT INTO vending_machine (vd_vending_machine_location, vd_vending_machine_address, vd_vending_machine_postal_code, "
                       "vd_vending_machine_city, vd_vending_machine_country) VALUES (%s, %s, %s, %s, %s)")
                cursor.execute(sql, (vending_location, vending_address, vending_postal_code, vending_city, vending_country))
                self.connection.commit()
                self.logger.log_debug(
                    f"Machine created: (Vending location:{vending_location}), (Vending address: {vending_address}), (Vending postal code: {vending_postal_code}), (Vending city: {vending_city}), (Vending country: {vending_country}")
            return True
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
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
            print(f"Error reading vending machines: {e}")
            return None

    def get_vending_machine_data(self, machine_name):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM vending_machine WHERE vd_vending_machine_location = %s"
                cursor.execute(sql, (machine_name,))
                machine_data = cursor.fetchone()
                return machine_data
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            # Handle the error (e.g., log it or show a message box)
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
                    print("Product already exists in the inventory for this vending machine.")
                    return False
                else:
                    # Insert the product into the inventory table for the vending machine
                    sql_insert = """
                            INSERT INTO inventory (vd_inventory_vending_machine_id, vd_inventory_product_id, vd_inventory_stock_quantity, vd_inventory_min_stock, vd_inventory_max_stock, vd_inventory_refill_stock) 
                            VALUES (%s, %s, 0, %s, %s, %s)
                        """
                    cursor.execute(sql_insert, (vending_machine_id, product_id, min_stock, max_stock, refill_stock))
                    self.connection.commit()
                    print("Product added to inventory for the vending machine.")
                    return True
        except pymysql.MySQLError as e:
            print(f"Error setting up vending machine: {e}")
            return False


def main():
    # Create an instance of the user_interface class
    ui = vending_machine_interface()

    # Call methods of the user_interface instance as needed
    ui.run_vending_machine_interface()

if __name__ == "__main__":
    main()