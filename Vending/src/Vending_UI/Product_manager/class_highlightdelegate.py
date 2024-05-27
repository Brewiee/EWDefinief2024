from PySide6.QtWidgets import QStyle,QStyledItemDelegate
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class HighlightDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        painter.save()
        if option.state & QStyle.State_Selected:
            # Set the background color when the item is selected
            painter.fillRect(option.rect, QColor("lightblue"))  # Change background color as desired
            painter.setPen(QColor("black"))  # Set text color
        else:
            # Use default background color when the item is not selected
            painter.fillRect(option.rect, option.palette.base())
            painter.setPen(option.palette.text().color())  # Use default text color
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, index.data())
        painter.restore()

