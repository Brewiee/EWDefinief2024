import pymysql
from Vending.Log_creator.class_custom_logger import CustomLogger


class database_connector:
    # initialize database connection and logger
    def __init__(self):
        self.connection = self.database_connection()
        self.logger = CustomLogger("Vending", "Logging")
        self.logger.log_error("Start Database Connector Error Log")

    def database_connection(self):
        try:
            # connect to the Mysql database
            connection = pymysql.connect(
                host= "localhost",
                user= "dbadmin",               # replace with your MySQL username
                password= "dbadmin",          # replace with your MySQL password
                database= "vending",        # current database
                charset= "utf8mb4",         # UTF-8 encoding scheme
                cursorclass= pymysql.cursors.DictCursor
            )
            return connection
        except pymysql.MySQLError as e:     # error handling
            self.logger.log_error(f"Error connecting to MySQL: {e}")
            return None
