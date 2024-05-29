import pymysql
from Vending.Database_connector.class_database_connector import database_connector
from Vending.Log_creator.class_custom_logger import CustomLogger

class product_interface:
    def __init__(self):
        self.logger = CustomLogger("Vending", "Logging")
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        self.logger.log_debug("Start Product Interface Debug Log")
        self.logger.log_info("Start Product Interface Info Log")
        self.logger.log_error("Start Product Interface Error Log")

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
                sql = """
                UPDATE product 
                SET vd_product_name=%s, vd_product_code=%s, vd_product_price=%s, vd_product_vat=%s 
                WHERE vd_product_id=%s
                """
                cursor.execute(sql, (product_name, product_code, product_price, product_vat, product_id))
                self.connection.commit()

                self.logger.log_info(
                    f"Product updated successfully: (Product ID: {product_id}), (Product code: {product_code}), "
                    f"(Product name: {product_name}), (Product price: {product_price}), (Product VAT: {product_vat})"
                )
            return True
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error updating product with ID {product_id}: {e}")
            return False
        except Exception as e:
            self.logger.log_error(f"Unexpected error updating product with ID {product_id}: {e}")
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