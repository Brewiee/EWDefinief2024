from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

class create_pdf:
    def __init__(self, data, headers, filename, title=None, save_path=None):
        self.data = data
        self.headers = headers
        self.filename = filename
        self.title = title
        self.save_path = save_path

    def generate_pdf(self):
        doc = SimpleDocTemplate(self.filename, pagesize=letter)

        elements = []

        # Create table for the title
        if self.title:
            title_table_data = [[self.title]]
            title_table = Table(title_table_data, colWidths=[500])
            title_style = [('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, -1), 16),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 12)]
            title_table.setStyle(TableStyle(title_style))
            elements.append(title_table)

        # Add table with data
        table_data = [self.headers] + self.data
        table = Table(table_data)

        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)
        elements.append(table)

        # Save the PDF file
        if self.save_path:
            pdf_output_path = os.path.join(self.save_path, self.filename)
        else:
            pdf_output_path = self.filename

        doc.build(elements)
        return pdf_output_path
