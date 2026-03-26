#!/usr/bin/env python
"""
IMDB API Collection Report Generator
Generates a professional PDF report for the IMDB API Postman collection.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os

# Color scheme
NAVY_BLUE = colors.HexColor('#1a3c5e')
LIGHT_GRAY = colors.HexColor('#f0f0f0')
DARK_GRAY = colors.HexColor('#333333')
WHITE = colors.white

# Method colors
METHOD_COLORS = {
    'GET': colors.HexColor('#28a745'),
    'POST': colors.HexColor('#007bff'),
    'PUT': colors.HexColor('#fd7e14'),
    'PATCH': colors.HexColor('#6f42c1'),
    'DELETE': colors.HexColor('#dc3545'),
}


class MethodBadge(Flowable):
    """A colored badge for HTTP methods."""
    
    def __init__(self, method, width=50, height=16):
        Flowable.__init__(self)
        self.method = method
        self.width = width
        self.height = height
        self.color = METHOD_COLORS.get(method, colors.gray)
    
    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, 0, self.width, self.height, 3, fill=1, stroke=0)
        self.canv.setFillColor(WHITE)
        self.canv.setFont('Helvetica-Bold', 8)
        text_width = self.canv.stringWidth(self.method, 'Helvetica-Bold', 8)
        self.canv.drawString((self.width - text_width) / 2, 4, self.method)


class HorizontalLine(Flowable):
    """A horizontal line flowable."""
    
    def __init__(self, width, color=NAVY_BLUE, thickness=2):
        Flowable.__init__(self)
        self.width = width
        self.color = color
        self.thickness = thickness
    
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def add_page_decorations(canvas, doc):
    """Add page number and top stripe to each page."""
    canvas.saveState()
    
    # Top stripe
    canvas.setFillColor(NAVY_BLUE)
    canvas.rect(0, letter[1] - 15, letter[0], 15, fill=1, stroke=0)
    
    # Page number
    canvas.setFillColor(DARK_GRAY)
    canvas.setFont('Helvetica', 9)
    page_num = f"Page {doc.page}"
    canvas.drawCentredString(letter[0] / 2, 30, page_num)
    
    canvas.restoreState()


def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='CoverTitle',
        parent=styles['Title'],
        fontSize=36,
        textColor=NAVY_BLUE,
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=20
    ))
    
    styles.add(ParagraphStyle(
        name='CoverDate',
        parent=styles['Normal'],
        fontSize=12,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=30
    ))
    
    styles.add(ParagraphStyle(
        name='CoverDescription',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        leading=16
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=NAVY_BLUE,
        spaceBefore=20,
        spaceAfter=15,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SubHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=NAVY_BLUE,
        spaceBefore=15,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='GroupHeader',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=NAVY_BLUE,
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='EndpointName',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_GRAY,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='EndpointURL',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#555555'),
        fontName='Courier'
    ))
    
    styles.add(ParagraphStyle(
        name='EndpointDesc',
        parent=styles['Normal'],
        fontSize=10,
        textColor=DARK_GRAY,
        spaceAfter=5
    ))
    
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontSize=9,
        textColor=DARK_GRAY,
        fontName='Courier',
        leftIndent=20,
        backColor=colors.HexColor('#f5f5f5'),
        borderPadding=5
    ))
    
    styles.add(ParagraphStyle(
        name='BodyText',
        parent=styles['Normal'],
        fontSize=10,
        textColor=DARK_GRAY,
        leading=14
    ))
    
    return styles


def create_cover_page(styles):
    """Create the cover page elements."""
    elements = []
    
    elements.append(Spacer(1, 2 * inch))
    elements.append(Paragraph("IMDB API", styles['CoverTitle']))
    elements.append(Paragraph("API Collection Report", styles['CoverSubtitle']))
    elements.append(Paragraph("2026-03-25", styles['CoverDate']))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(HorizontalLine(400))
    elements.append(Spacer(1, 0.5 * inch))
    
    description = """This report documents the REST API endpoints for the IMDB-like application 
    built with Django REST Framework. It covers Watchlist and Stream Platform resources."""
    elements.append(Paragraph(description, styles['CoverDescription']))
    
    elements.append(PageBreak())
    return elements


def create_overview_section(styles):
    """Create the overview section."""
    elements = []
    
    elements.append(Paragraph("Section 1 — Overview", styles['SectionHeader']))
    
    # Collection info
    info_data = [
        ['Collection Name:', 'IMDB API'],
        ['Base URL:', 'http://127.0.0.1:8000'],
        ['Total Endpoints:', '9'],
        ['Framework:', 'Django REST Framework'],
        ['Environment:', 'IMDB Local'],
    ]
    
    info_table = Table(info_data, colWidths=[150, 300])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3 * inch))
    
    # Environment Variables
    elements.append(Paragraph("Environment Variables", styles['SubHeader']))
    
    env_data = [
        ['Variable', 'Default Value'],
        ['baseUrl', 'http://127.0.0.1:8000'],
        ['movie_id', '1'],
        ['platform_id', '1'],
    ]
    
    env_table = Table(env_data, colWidths=[150, 300])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(env_table)
    
    elements.append(PageBreak())
    return elements


def create_endpoint_entry(num, method, url, name, description, body=None, styles=None):
    """Create a single endpoint entry."""
    elements = []
    
    # Method badge and name
    method_color = METHOD_COLORS.get(method, colors.gray)
    badge_html = f'<font face="Helvetica-Bold" size="10" color="white"><b>{method}</b></font>'
    
    # Create a table for method badge + endpoint info
    endpoint_text = f'<b>{num}. {name}</b>'
    url_text = f'<font face="Courier" size="9" color="#555555">{url}</font>'
    
    elements.append(Spacer(1, 8))
    
    # Method badge as colored text
    method_style = ParagraphStyle(
        name=f'Method{method}',
        fontSize=9,
        textColor=WHITE,
        backColor=method_color,
        fontName='Helvetica-Bold',
        leftIndent=5,
        rightIndent=5,
        spaceBefore=2,
        spaceAfter=2,
    )
    
    # Combine method and name
    header_text = f'<font face="Helvetica-Bold" color="{method_color.hexval()}">[{method}]</font> <b>{name}</b>'
    elements.append(Paragraph(header_text, styles['EndpointName']))
    elements.append(Paragraph(url, styles['EndpointURL']))
    elements.append(Paragraph(description, styles['EndpointDesc']))
    
    if body:
        elements.append(Spacer(1, 5))
        elements.append(Paragraph("<b>Request Body:</b>", styles['BodyText']))
        # Format JSON with proper indentation
        code_lines = body.split('\n')
        for line in code_lines:
            elements.append(Paragraph(line.replace(' ', '&nbsp;'), styles['CodeBlock']))
    
    elements.append(Spacer(1, 10))
    return elements


def create_endpoints_section(styles):
    """Create the API endpoints section."""
    elements = []
    
    elements.append(Paragraph("Section 2 — API Endpoints", styles['SectionHeader']))
    
    # Group: General
    elements.append(Paragraph("Group: General", styles['GroupHeader']))
    elements.extend(create_endpoint_entry(
        1, 'GET', '/', 'API Root',
        'Returns links to the main API resources (watchlist and streamplatform).',
        styles=styles
    ))
    
    # Group: Watchlist
    elements.append(Paragraph("Group: Watchlist", styles['GroupHeader']))
    elements.extend(create_endpoint_entry(
        2, 'GET', '/list/', 'Get All Movies',
        'Returns a list of all watchlist items.',
        styles=styles
    ))
    elements.extend(create_endpoint_entry(
        3, 'GET', '/list/{{movie_id}}/', 'Get Movie Detail',
        'Returns details of a specific watchlist item by ID.',
        styles=styles
    ))
    
    # Group: Stream Platform
    elements.append(Paragraph("Group: Stream Platform", styles['GroupHeader']))
    elements.extend(create_endpoint_entry(
        4, 'GET', '/stream/', 'List Stream Platforms',
        'Returns a list of all streaming platforms.',
        styles=styles
    ))
    
    post_body = '''{
  "name": "Netflix",
  "about": "A popular streaming service",
  "website": "https://www.netflix.com"
}'''
    elements.extend(create_endpoint_entry(
        5, 'POST', '/stream/', 'Create Stream Platform',
        'Creates a new streaming platform.',
        body=post_body,
        styles=styles
    ))
    
    elements.extend(create_endpoint_entry(
        6, 'GET', '/stream/{{platform_id}}/', 'Get Stream Platform Detail',
        'Returns details of a specific streaming platform by ID.',
        styles=styles
    ))
    
    put_body = '''{
  "name": "Netflix",
  "about": "Updated description",
  "website": "https://www.netflix.com"
}'''
    elements.extend(create_endpoint_entry(
        7, 'PUT', '/stream/{{platform_id}}/', 'Update Stream Platform',
        'Fully updates a streaming platform by ID.',
        body=put_body,
        styles=styles
    ))
    
    patch_body = '''{
  "about": "Partially updated description"
}'''
    elements.extend(create_endpoint_entry(
        8, 'PATCH', '/stream/{{platform_id}}/', 'Partial Update Stream Platform',
        'Partially updates a streaming platform by ID.',
        body=patch_body,
        styles=styles
    ))
    
    elements.extend(create_endpoint_entry(
        9, 'DELETE', '/stream/{{platform_id}}/', 'Delete Stream Platform',
        'Deletes a streaming platform by ID.',
        styles=styles
    ))
    
    elements.append(PageBreak())
    return elements


def create_data_models_section(styles):
    """Create the data models section."""
    elements = []
    
    elements.append(Paragraph("Section 3 — Data Models", styles['SectionHeader']))
    
    # Watchlist model
    elements.append(Paragraph("watchlist", styles['SubHeader']))
    
    watchlist_data = [
        ['Field', 'Type', 'Notes'],
        ['id', 'Integer', 'Auto-generated, read-only'],
        ['title', 'String', 'max_length=50'],
        ['story_line', 'String', 'max_length=100'],
        ['plateform', 'FK → streamplatform', 'on_delete=CASCADE'],
        ['active', 'Boolean', 'default=True'],
        ['created', 'DateTime', 'auto_now_add, read-only'],
    ]
    
    watchlist_table = Table(watchlist_data, colWidths=[100, 130, 220])
    watchlist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(watchlist_table)
    elements.append(Spacer(1, 0.4 * inch))
    
    # Stream Platform model
    elements.append(Paragraph("streamplatform", styles['SubHeader']))
    
    stream_data = [
        ['Field', 'Type', 'Notes'],
        ['id', 'Integer', 'Auto-generated, read-only'],
        ['name', 'String', 'max_length=50'],
        ['about', 'String', 'max_length=100'],
        ['website', 'URL', 'max_length=200'],
        ['watch_list', 'Reverse FK', 'StringRelated, read-only'],
    ]
    
    stream_table = Table(stream_data, colWidths=[100, 130, 220])
    stream_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_GRAY),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Courier'),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), DARK_GRAY),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(stream_table)
    
    return elements


def generate_report(output_path):
    """Generate the complete PDF report."""
    # Create the document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )
    
    # Create styles
    styles = create_styles()
    
    # Build document elements
    elements = []
    
    # Cover page
    elements.extend(create_cover_page(styles))
    
    # Overview section
    elements.extend(create_overview_section(styles))
    
    # Endpoints section
    elements.extend(create_endpoints_section(styles))
    
    # Data models section
    elements.extend(create_data_models_section(styles))
    
    # Build the PDF
    doc.build(elements, onFirstPage=add_page_decorations, onLaterPages=add_page_decorations)
    
    print(f"PDF report generated successfully: {output_path}")
    return True


if __name__ == '__main__':
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'IMDB_API_Collection_Report.pdf')
    
    generate_report(output_file)
