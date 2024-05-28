import pymysql
from Vending.Database_connector.class_database_connector import database_connector
from Vending.Log_creator.class_custom_logger import CustomLogger

class product_interface:
    def __init__(self):
        self.logger = CustomLogger("Product_interface", "Logging")
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        self.logger.log_debug("Start Product Interface Debug Log")
        self.logger.log_info("Start Product Interface Info Log")
        self.logger.log_error("Start Product Interface Error Log")

    def run_crud_product_interface(self):
        while True:
            print("\nProduct Interface:")
            print("1. Create product")
            print("2. Read products")
            print("3. Update product")
            print("4. Delete product")
            print("5. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                product_code = input("Enter product code: ")
                product_name = input("Enter product name: ")
                product_price = float(input("Enter product price: "))
                product_vat = float(input("Enter product tax: "))
                success = self.create_product(product_code, product_name, product_price, product_vat)
                if success:
                    print("Product created successfully!")
            elif choice == "2":
                self.read_products()
            elif choice == "3":
                product_id = input("Enter product ID to update: ")
                product_name = input("Enter new product name: ")
                product_price = float(input("Enter new product price: "))
                product_vat = float(input("Enter new product tax: "))
                success = self.update_product(product_id, product_name, product_price, product_vat)
                if success:
                    print("Product updated successfully!")
            elif choice == "4":
                product_id = input("Enter product ID to delete: ")
                success = self.delete_product(product_id)
                if success:
                    print("Product deleted successfully!")
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

    def create_product(self, product_code, product_name, product_price, product_vat):
        try:
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO product (vd_product_code, vd_product_name, vd_product_price, vd_product_vat) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (product_code, product_name, product_price, product_vat))
                self.connection.commit()
                self.logger.log_info(f"Product created: (Product code:{product_code}), (Product name: {product_name}), (Product price: {product_price}), (Product VAT: {product_vat})")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error creating product: {e}")
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
                        product_code = product['vd_product_code']
                        product_name = product['vd_product_name']
                        product_price = product['vd_product_price']
                        product_vat = product['vd_product_vat']
                        product_data.append((product_id, product_code, product_name, product_price, product_vat))
                return product_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error reading products: {e}")
            return None

    def update_product(self, product_id, product_code, product_name, product_price, product_vat):
        try:
            with self.connection.cursor() as cursor:
                sql = "UPDATE product SET vd_product_name=%s, vd_product_code=%s, vd_product_price=%s, vd_product_vat=%s WHERE vd_product_id=%s"
                cursor.execute(sql, (product_name, product_code, product_price, product_vat, product_id))
                self.connection.commit()
                self.logger.log_info(
                    f"Product updated: (Product code:{product_code}), (Product name: {product_name}), (Product price: {product_price}), (Product VAT: {product_vat})")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating product: {e}")
            return False

    def delete_product(self, product_id):
        try:
            with self.connection.cursor() as cursor:
                sql = "DELETE FROM product WHERE vd_product_id=%s"
                cursor.execute(sql, (product_id,))
                self.connection.commit()
                self.logger.log_info(f"Product deleted: Product name: {product_id}")
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error deleting product: {e}")
            return False

def main():
    # Create an instance of the user_interface class
    ui = product_interface()

    # Call methods of the user_interface instance as needed
    ui.run_crud_product_interface()

if __name__ == "__main__":
    main()
"""
                def generate_product_code(cursor):
                    cursor.execute("SELECT MAX(vd_product_id) FROM product")
                    result = cursor.fetchone()
                    print("Result:", result)  # Debug print
                    if result and 'MAX(vd_product_id)' in result:
                        max_id = result['MAX(vd_product_id)']
                    else:
                        max_id = 0
                    print("Max ID:", max_id)  # Debug print
                    next_id = max_id + 1
                    return f"PROD{next_id:03}"
"""


