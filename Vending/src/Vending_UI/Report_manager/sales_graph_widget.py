from PySide6.QtWidgets import QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import mplcursors  # Import mplcursors library
class SalesGraphWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = plt.figure(figsize=(7, 5))
        self.canvas = FigureCanvas(self.figure)
        layout = QHBoxLayout(self)
        layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)

    def update_graph(self, sales_data):
        self.ax.clear()

        # Extract data for plotting
        sales_dates = [data[0] for data in sales_data]
        total_sold = [data[1] for data in sales_data]
        total_price = [data[2] for data in sales_data]

        # Plot total sold
        self.ax.bar(sales_dates, total_sold, color='blue', alpha=0.7, label='Total Sold')

        # Plot total price as a separate bar plot
        self.ax.bar(sales_dates, total_price, color='green', alpha=0.7, label='Total Price')

        # Set labels and title
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Values')
        self.ax.set_title('Sales Graph')

        # Rotate x-axis labels for better readability
        self.ax.tick_params(axis='x', rotation=45)

        # Show legend
        self.ax.legend()

        # Format x-axis date labels
        self.figure.autofmt_xdate()

        # Update canvas
        self.canvas.draw()














