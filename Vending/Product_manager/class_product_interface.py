import pymysql
from Vending.Database_connector.class_database_connector import database_connector
from Vending.Log_creator.class_custom_logger import CustomLogger


class product_interface:
    def __init__(self):
        # Initialize the custom logger for logging activities
        self.logger = CustomLogger("Vending", "Logging")

        # Initialize database connection using the database connector class
        db_connector = database_connector()
        self.connection = db_connector.database_connection()

        # Log the start of the Product Interface logs at different levels
        self.logger.log_debug("Start Product Interface Debug Log")
        self.logger.log_info("Start Product Interface Info Log")
        self.logger.log_error("Start Product Interface Error Log")

    def create_product(self, product_code, product_name, product_price, product_vat):
        """
        Create a new product in the database with the provided details.
        """
        try:
            with self.connection.cursor() as cursor:
                # Fetch the maximum existing product ID
                cursor.execute("SELECT COALESCE(MAX(vd_product_id), 0) AS max_id FROM product")
                result = cursor.fetchone()
                last_id = result['max_id']
                new_id = last_id + 1

                # SQL query to insert a new product into the product table
                sql = "INSERT INTO product (vd_product_id, vd_product_code, vd_product_name, vd_product_price, vd_product_vat) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (new_id, product_code, product_name, product_price, product_vat))
                self.connection.commit()

                # Log successful product creation
                self.logger.log_info(
                    f"Product created: (Product ID: {new_id}), (Product code: {product_code}), (Product name: {product_name}), (Product price: {product_price}), (Product VAT: {product_vat})"
                )
            return True
        except pymysql.MySQLError as e:
            # Log any SQL errors that occur during product creation
            self.logger.log_error(f"Error creating product: {e}")
            return False

    def read_products(self):
        """
        Read all products from the database and return them as a list of tuples.
        """
        try:
            with self.connection.cursor() as cursor:
                # SQL query to select all products from the product table
                sql = "SELECT * FROM product"
                cursor.execute(sql)
                products = cursor.fetchall()

                # Process the retrieved products and format them into a list of tuples
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
            # Log any SQL errors that occur during reading products
            self.logger.log_error(f"Error reading products: {e}")
            return None

    def update_product(self, product_id, product_code, product_name, product_price, product_vat):
        """
        Update the details of an existing product in the database.
        """
        try:
            with self.connection.cursor() as cursor:
                # SQL query to update the product details
                sql = """
                UPDATE product 
                SET vd_product_name=%s, vd_product_code=%s, vd_product_price=%s, vd_product_vat=%s 
                WHERE vd_product_id=%s
                """
                cursor.execute(sql, (product_name, product_code, product_price, product_vat, product_id))
                self.connection.commit()

                # Log successful product update
                self.logger.log_info(
                    f"Product updated successfully: (Product ID: {product_id}), (Product code: {product_code}), "
                    f"(Product name: {product_name}), (Product price: {product_price}), (Product VAT: {product_vat})"
                )
            return True
        except pymysql.MySQLError as e:
            # Log any SQL errors that occur during product update
            self.logger.log_error(f"Error updating product with ID {product_id}: {e}")
            return False
        except Exception as e:
            # Log any unexpected errors that occur during product update
            self.logger.log_error(f"Unexpected error updating product with ID {product_id}: {e}")
            return False

    def delete_product(self, product_id):
        """
        Delete a product and its related inventory items from the database.
        """
        try:
            with self.connection.cursor() as cursor:
                # First, update related rows in the invoice table to set vd_invoice_product_id to NULL
                update_invoice_sql = "UPDATE invoice SET vd_invoice_product_id=NULL WHERE vd_invoice_product_id=%s"
                cursor.execute(update_invoice_sql, (product_id,))

                # Then delete related rows in the inventory table
                inventory_sql = "DELETE FROM inventory WHERE vd_inventory_product_id=%s"
                cursor.execute(inventory_sql, (product_id,))

                # second, update related rows in the supplier table to set vd_supplier_product_id to NULL
                update_invoice_sql = "UPDATE supplier SET vd_supplier_product_id=NULL WHERE vd_supplier_product_id=%s"
                cursor.execute(update_invoice_sql, (product_id,))

                # Then delete related rows in the supplier table
                inventory_sql = "DELETE FROM supplier WHERE vd_supplier_product_id=%s"
                cursor.execute(inventory_sql, (product_id,))

                # Now delete the product
                product_sql = "DELETE FROM product WHERE vd_product_id=%s"
                cursor.execute(product_sql, (product_id,))

                # Commit the transaction
                self.connection.commit()

                # Log successful product deletion
                self.logger.log_info(f"Product deleted: Product ID: {product_id}")
                return True
        except pymysql.MySQLError as e:
            # Log any SQL errors that occur during product deletion
            self.logger.log_error(f"Error deleting product: {e}")
            print(f"Error deleting product ID: {product_id}, error: {e}")
            return False
