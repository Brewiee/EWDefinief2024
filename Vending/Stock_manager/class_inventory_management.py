from Vending.Database_connector.class_database_connector import database_connector
import pymysql

class stock_manager:
    def __init__(self):
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        print("inventory manager")

    def run_stock_manager(self):
        while True:
            print("\nStock Manager:")
            print("1. Choose vending machine")
            print("2. read inventory")
            print("3. update stock quantity")
            print("4. set refill stock")
            print("5. set maximum stock")
            print("6. set minimum stock")
            print("7. set stock to refill")
            print("8. set stock to max")
            print("9. show stock to refill")
            print("10. show stock to max")
            print("11. back to main menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.choose_vending_machine()
            elif choice == "2":
                self.read_inventory()
            elif choice == "3":
                product_id = int(input("Which id do you want to set stock quantity? "))
                new_stock_quantity = int(input("What is the new stock quantity? "))
                self.update_stock_quantity(product_id, new_stock_quantity)
            elif choice == "4":
                product_id = int(input("Which id do you want to set refill stock quantity? "))
                new_refill_stock_quantity = int(input("What is the new refill stock quantity? "))
                self.set_refill_stock(product_id, new_refill_stock_quantity)
            elif choice == "5":
                product_id = int(input("Which id do you want to set stock quantity? "))
                new_max_stock_quantity = int(input("What is the new maximum stock quantity? "))
                self.set_max_stock(product_id, new_max_stock_quantity)
            elif choice == "6":
                product_id = int(input("Which id do you want to set stock quantity? "))
                new_min_stock_quantity = int(input("What is the new minimum stock quantity? "))
                self.set_min_stock(product_id, new_min_stock_quantity)
            elif choice == "7":
                self.set_stock_to_refill()
            elif choice == "8":
                self.set_stock_to_max()
            elif choice == "9":
                self.show_stock_to_refill()
            elif choice == "10":
                self.show_stock_to_max()
            elif choice == "11":
                break
            else:
                print("Invalid choice. Please try again.")

    def choose_vending_machine(self):
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
                        vending_machine_data.append((inventory_id, vending_location))  # Use [] to append as a tuple
                return vending_machine_data
        except pymysql.MySQLError as e:
            print(f"Error reading vending machines: {e}")
            return None

    def read_inventory(self, vending_machine_id=None):
        print(f"the id is {vending_machine_id}")
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
            print(f"Error reading products: {e}")
            return None

    def update_stock_quantity(self, inventory_id, inventory_stock_quantity):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_stock_quantity=%s WHERE vd_inventory_id=%s"
                cursor.execute(sql, (inventory_stock_quantity, inventory_id))
                self.connection.commit()
                print("Stock updated")
            return True
        except pymysql.MySQLError as e:
            print(f"Error updating stock quantity: {e}")
            return False

    def set_refill_stock(self, inventory_product_id, inventory_refill_stock):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_refill_stock=%s WHERE vd_inventory_product_id=%s"
                cursor.execute(sql, (inventory_refill_stock, inventory_product_id))
                self.connection.commit()
                print("Refill stock updated")
            return True
        except pymysql.MySQLError as e:
            print(f"Error updating refill stock: {e}")
            return False

    def set_max_stock(self, inventory_product_id, inventory_max_stock):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_max_stock=%s WHERE vd_inventory_product_id=%s"
                cursor.execute(sql, (inventory_max_stock, inventory_product_id))
                self.connection.commit()
                print("Max stock updated")
            return True
        except pymysql.MySQLError as e:
            print(f"Error updating max stock: {e}")
            return False

    def set_min_stock(self, inventory_product_id, inventory_min_stock):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_min_stock=%s WHERE vd_inventory_product_id=%s"
                cursor.execute(sql, (inventory_min_stock, inventory_product_id))
                self.connection.commit()
                print("Min stock updated")
            return True
        except pymysql.MySQLError as e:
            print(f"Error updating min stock: {e}")
            return False

    def set_stock_to_refill(self, vending_machine_id):
        print(f"this id is {vending_machine_id}")
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_stock_quantity = vd_inventory_refill_stock WHERE vd_inventory_vending_machine_id = %s"
                cursor.execute(sql, (vending_machine_id,))
                self.connection.commit()
                print("Stock set to refill values")
            return True
        except pymysql.MySQLError as e:
            print(f"Error setting stock to refill: {e}")
            return False  # Return False in case of an error

    def set_stock_to_max(self, vending_machine_id):
        print(vending_machine_id)
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE inventory SET vd_inventory_stock_quantity = vd_inventory_max_stock WHERE vd_inventory_vending_machine_id = %s"
                cursor.execute(sql, (vending_machine_id,))
                self.connection.commit()
                print("Stock set to max values")
            return True
        except pymysql.MySQLError as e:
            print(f"Error setting stock to max: {e}")
            return False  # Return False in case of an error

    def show_stock_to_refill(self, vending_machine_id):
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
            print(f"Error connecting: {e}")

    def show_stock_to_max(self, vending_machine_id):
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
            print(f"Error connecting: {e}")

    def update_inventory(self, inventory_id, edited_data):
        try:
            with self.connection.cursor() as cursor:
                # Construct the SQL UPDATE query
                sql = """
                    UPDATE inventory
                    SET vd_inventory_stock_quantity = %s,
                        vd_inventory_refill_stock = %s,
                        vd_inventory_max_stock = %s,
                        vd_inventory_min_stock = %s
                    WHERE vd_inventory_id = %s
                """
                # Execute the SQL query with the edited data
                cursor.execute(sql, (*edited_data, inventory_id))
                # Commit the transaction if necessary
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(f"Error updating inventory: {e}")

def main():
    ui = stock_manager()
    ui.run_stock_manager()

if __name__ == "__main__":
    main()
