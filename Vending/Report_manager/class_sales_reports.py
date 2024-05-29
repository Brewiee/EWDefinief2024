import pymysql
from Vending.Database_connector.class_database_connector import database_connector
from Vending.Log_creator.class_custom_logger import CustomLogger

class sales_report_manager:
    def __init__(self):
        db_connector = database_connector()
        self.connection = db_connector.database_connection()
        self.logger = CustomLogger("Vending", "Logging")
        self.logger.log_info("Start Report Interface Info Logging")
        self.logger.log_error("Start Report Interface Error Logging")

    def overall_sales_report(self, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    WITH date_range AS (
                        SELECT %s AS start_date, %s AS end_date)
                    SELECT p.vd_product_name, 
                           COUNT(*) AS total_sold,
                           SUM(p.vd_product_price) AS total_price,
                           ROUND(SUM(p.vd_product_price * (p.vd_product_vat / 100)), 2) AS total_vat
                    FROM invoice i
                    JOIN product p ON i.vd_invoice_product_id = p.vd_product_id
                    CROSS JOIN 
                        date_range
                    WHERE i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                    GROUP BY 
                        p.vd_product_name
                    UNION ALL
                    SELECT 
                        'total',
                        COUNT(*),
                        SUM(p.vd_product_price),
                        ROUND(SUM(p.vd_product_price * p.vd_product_vat / 100), 2)
                    FROM invoice i
                    JOIN product p ON i.vd_invoice_product_id = p.vd_product_id
                    CROSS JOIN
                        date_range
                    WHERE i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date;
                    """
                cursor.execute(sql, (start_date, end_date))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    product_name = data["vd_product_name"]
                    total_sold = data["total_sold"]
                    total_price = data["total_price"]
                    total_vat = data["total_vat"]
                    sales_data.append((product_name, total_sold, total_price, total_vat))

                # Sort the data based on the total price column
                sales_data.sort(key=lambda x: x[2], reverse=True)  # Sort based on the third element (total_price)

                # Move the "total" row to the last position
                total_row = [row for row in sales_data if row[0] == 'total']
                if total_row:
                    sales_data.remove(total_row[0])
                    sales_data.append(total_row[0])
                return sales_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def overall_sales_graph(self, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                WITH date_range AS (SELECT %s AS start_date, %s AS end_date)
                SELECT 
                    DATE(i.vd_invoice_date) AS sales_date,
                    COUNT(*) AS total_sold,
                    SUM(p.vd_product_price) AS total_price
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                CROSS JOIN 
                    date_range
                WHERE 
                    i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                GROUP BY 
                    sales_date;
                """
                cursor.execute(sql, (start_date, end_date))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    # No need to convert the date format, as it's already in datetime.date format
                    sales_date = data["sales_date"]
                    total_sold = data["total_sold"]
                    total_price = data["total_price"]
                    sales_data.append((sales_date, total_sold, total_price))
                return sales_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def top_three_products(self, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                WITH date_range AS (SELECT %s AS start_date, %s AS end_date)
                SELECT 
                    p.vd_product_name,
                    COUNT(*) AS total_sold
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                CROSS JOIN 
                    date_range
                WHERE 
                    i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                GROUP BY 
                    p.vd_product_name
                ORDER BY 
                    COUNT(*) DESC
                LIMIT 3;
                """
                cursor.execute(sql, (start_date, end_date))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    product_name = data["vd_product_name"]
                    total_sold = data["total_sold"]
                    sales_data.append((product_name, total_sold))
                return(sales_data)
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def top_three_vending_machines(self, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                WITH date_range AS (SELECT %s AS start_date, %s AS end_date)
                SELECT 
                    v.vd_vending_machine_id,
                    v.vd_vending_machine_location,
                    COUNT(*) AS total_sold
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                JOIN 
                    vending_machine v ON i.vd_invoice_vending_machine_id = v.vd_vending_machine_id
                CROSS JOIN 
                    date_range
                WHERE 
                    i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                GROUP BY 
                    v.vd_vending_machine_id, v.vd_vending_machine_location
                ORDER BY 
                    COUNT(*) DESC
                LIMIT 3;
                """
                cursor.execute(sql, (start_date, end_date))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    vending_machine_id = data["vd_vending_machine_id"]
                    vending_machine_location = data["vd_vending_machine_location"]
                    total_sold = data["total_sold"]
                    sales_data.append((vending_machine_id, vending_machine_location, total_sold))
                return(sales_data)
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def sales_report(self, vending_machine, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                # Query for a specific vending machine
                sql = """
                WITH date_range AS (
                SELECT %s AS start_date, %s AS end_date
                )
                SELECT 
                    p.vd_product_name, 
                    COUNT(*) AS total_sold,
                    SUM(p.vd_product_price) AS total_price,
                    ROUND(SUM(p.vd_product_price * (p.vd_product_vat / 100)), 2) AS total_vat
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                JOIN
                    date_range ON i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                WHERE 
                    i.vd_invoice_vending_machine_id = %s
                GROUP BY 
                    p.vd_product_name

                UNION ALL

                SELECT 
                    'total',
                    COUNT(*) AS total_sold,
                    SUM(p.vd_product_price) AS total_price,
                    ROUND(SUM(p.vd_product_price * (p.vd_product_vat / 100)), 2) AS total_vat
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                JOIN
                    date_range ON i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                WHERE 
                    i.vd_invoice_vending_machine_id = %s;
                """
                cursor.execute(sql, (start_date, end_date, vending_machine, vending_machine))

                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    product_name = data["vd_product_name"]
                    total_sold = data["total_sold"]
                    total_price = data["total_price"]
                    total_vat = data["total_vat"]
                    sales_data.append((product_name, total_sold, total_price, total_vat))
                return sales_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def sales_graph(self, vending_machine, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                WITH date_range AS (
                    SELECT %s AS start_date, %s AS end_date
                )
                SELECT 
                    DATE(i.vd_invoice_date) AS sales_date,
                    COUNT(*) AS total_sold,
                    SUM(p.vd_product_price) AS total_price
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                JOIN 
                    date_range ON i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                WHERE 
                    i.vd_invoice_vending_machine_id = %s
                GROUP BY 
                    sales_date;
                """
                cursor.execute(sql, (start_date, end_date, vending_machine))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    sales_date = data["sales_date"]
                    total_sold = data["total_sold"]
                    total_price = data["total_price"]
                    sales_data.append((sales_date, total_sold, total_price))
                return sales_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def vat_report(self, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                WITH date_range AS (SELECT %s AS start_date, %s AS end_date)
                SELECT 
                    COUNT(*) AS total_sold,
                    SUM(p.vd_product_price) AS total_price,
                    ROUND(SUM(p.vd_product_price * (p.vd_product_vat / 100)), 2) AS total_vat
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                JOIN 
                    date_range ON i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                """
                cursor.execute(sql, (start_date, end_date))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    total_sold = data["total_sold"]
                    total_price = data["total_price"]
                    total_vat = data["total_vat"]
                    sales_data.append((total_sold, total_price, total_vat))
                return(sales_data)
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def payment_method_report(self, start_date, end_date):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                WITH date_range AS (SELECT %s AS start_date, %s AS end_date)
                SELECT 
                    pm.vd_payment_method,
                    COUNT(*) AS total_sold,
                    SUM(p.vd_product_price) AS total_price
                FROM 
                    invoice i
                JOIN 
                    product p ON i.vd_invoice_product_id = p.vd_product_id
                JOIN 
                    date_range ON i.vd_invoice_date BETWEEN date_range.start_date AND date_range.end_date
                JOIN 
                    payment pm ON i.vd_invoice_payment_id = pm.vd_payment_id
                GROUP BY 
                    pm.vd_payment_method, i.vd_invoice_payment_id
                HAVING
                    pm.vd_payment_method IN ('Cash', 'Cashless');
                """
                cursor.execute(sql, (start_date, end_date))
                sales = cursor.fetchall()
                sales_data = []
                for data in sales:
                    payment_method = data["vd_payment_method"]
                    total_sold = data["total_sold"]
                    total_price = data["total_price"]
                    sales_data.append((payment_method, total_sold, total_price))
                return(sales_data)
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error retrieving sales data: {e}")
            return None

    def choose_vending_machine(self):
        try:
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT DISTINCT i.vd_invoice_vending_machine_id,
                                    p.vd_vending_machine_location
                    FROM invoice i
                    INNER JOIN vending_machine p ON i.vd_invoice_vending_machine_id = p.vd_vending_machine_id;
                """
                cursor.execute(sql)
                vending_machine = cursor.fetchall()
                vending_machine_data = []
                if vending_machine:
                    for machine in vending_machine:
                        invoice_id = machine["vd_invoice_vending_machine_id"]
                        vending_location = machine["vd_vending_machine_location"]
                        vending_machine_data.append((invoice_id, vending_location))  # Use [] to append as a tuple
                return vending_machine_data
        except pymysql.MySQLError as e:
            self.logger.log_error(f"Error reading vending machines: {e}")
            return None