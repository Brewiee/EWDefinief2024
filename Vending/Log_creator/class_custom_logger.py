import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, gui_name, log_dir):
        self.gui_name = gui_name
        self.log_dir = log_dir

        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Construct the log directory path
        log_dir_path = os.path.join(os.getcwd(), log_dir)

        # Configure debug log file
        debug_log_filename = os.path.join(log_dir_path, f'{current_date}_{gui_name}_debug.log')
        debug_log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(filename=debug_log_filename, level=logging.DEBUG, format=debug_log_format)

        # Create a separate logger for info log file
        self.info_logger = logging.getLogger(f'{gui_name}_info_logger')
        self.info_logger.setLevel(logging.INFO)

        # Configure info log file
        info_log_filename = os.path.join(log_dir_path, f'{current_date}_{gui_name}_info.log')
        info_log_format = '%(asctime)s - %(levelname)s - %(message)s'
        info_handler = logging.FileHandler(filename=info_log_filename)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(logging.Formatter(info_log_format))
        self.info_logger.addHandler(info_handler)

        # Create a separate logger for error log file
        self.error_logger = logging.getLogger(f'{gui_name}_error_logger')
        self.error_logger.setLevel(logging.ERROR)

        # Configure error log file
        error_log_filename = os.path.join(log_dir_path, f'{current_date}_{gui_name}_error.log')
        error_log_format = '%(asctime)s - %(levelname)s - %(message)s'
        error_handler = logging.FileHandler(filename=error_log_filename)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(logging.Formatter(error_log_format))
        self.error_logger.addHandler(error_handler)

    def log_debug(self, message):
        logging.debug(message)

    def log_info(self, message):
        self.info_logger.info(message)

    def log_error(self, message):
        self.error_logger.error(message)
