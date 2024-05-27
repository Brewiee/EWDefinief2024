class superadminstylesheet:

    @staticmethod
    def central_widget():
        return """
        background-color: #1F3F49;
        """
    @staticmethod
    def pushbutton():
        return """
        QPushButton {
            background-color: #1F3F49; 
            border: 2px solid #23282D; 
            color: #CED2CC; /* Light Gray */
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 10px; /* Add rounded corners */
        }

        QPushButton:hover {
            background-color: #DBAE58; /* Dark Blue */
            color: #1F3F49; /* Yellow Green */
        }

        QPushButton:pressed {
            background-color: #DADADA; /* Red */
        }
        """



    @staticmethod
    def label():
        return """
        QLabel {
            color: #CED2CC; /* Light Gray */
            font-size: 16px;
        }
        """

    @staticmethod
    def line_edit():
        return """
        QLineEdit {
            background-color: #FFFFFF; /* White */
            border: 2px solid #23282D; /* Dark Gray */
            color: #000000; /* Black */
            padding: 8px;
            font-size: 16px;
        }

        QLineEdit:hover {
            border-color: #DBAE58; /* Vivid Blue */
        }
        """

    @staticmethod
    def combo_box():
        return """
        QComboBox {
            background-color: #FFFFFF; /* White */
            border: 2px solid #23282D; /* Dark Gray */
            color: #000000; /* Black */
            padding: 8px;
            font-size: 16px;
        }
        
        QComboBox:hover {
            border-color: #DBAE58; /* Vivid Blue */
        }
        
        QComboBox:item {
        background-color: #DBAE58; /* Vivid Blue */
        color: #FFFFFF; /* Black */
    }
        """

    @staticmethod
    def set_combo_box_item_stylesheet(combo_box):
        combo_box.view().setStyleSheet("""
                QListView {
                    background-color: #DBAE58; /* Vivid Blue */
                    color: #FFFFFF; /* White */
                }
            """)
    @staticmethod
    def message_box():
        return """
        QMessageBox {
            background-color: #1F3F49; /* White */
            border: 2px solid #23282D; /* Dark Gray */
            color: #FFFFFF; /* Black */
            padding: 8px;
            font-size: 16px;
        }

        QMessageBox QPushButton {
            background-color: #1F3F49; /* Vivid Blue */
            border: 2px solid #23282D; /* Dark Gray */
            color: #CED2CC; /* Light Gray */
            padding: 8px 16px;
            font-size: 16px;
        }

        QMessageBox QPushButton:hover {
            background-color: #DBAE58; /* Dark Blue */
            color: #FFFFFF; /* Yellow Green */
        }

        QMessageBox QPushButton:pressed {
            background-color: #DADADA; /* Red */
        }
        """
