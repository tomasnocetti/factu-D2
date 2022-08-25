from cgitb import text
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from reportlab.pdfgen.canvas import Canvas
width, height = A4  # keep for later

styleSheet = getSampleStyleSheet()
style = styleSheet['BodyText']

canv = Canvas('doc.pdf', bottomup=0)

STROKE_COLOR = '#343434'
SROKE_WITH = 0.4
STRONG_STROKE = 0.6
FONT = 'Helvetica'
BOLD_FONT = 'Helvetica-Bold'
TOP_MARGIN = 21
LEFT_MARGIN = 15
HEADER_HEIGHT = 146


def generate_page_structure(canv, type, page_n):
    canv.setFont(BOLD_FONT, 22)

    canv.setLineWidth(SROKE_WITH)
    canv.setStrokeColor(STROKE_COLOR)
    canv.rect(LEFT_MARGIN, TOP_MARGIN, width -
              LEFT_MARGIN * 2, HEADER_HEIGHT, stroke=1)

    # Central divider inside header
    canv.line(width/2, 90, width/2, 167)

    # Horizonal divider inside header
    canv.setFont(BOLD_FONT, 16)
    canv.drawCentredString(width/2, 42, page_n)
    canv.line(LEFT_MARGIN, 49, width - LEFT_MARGIN, 49)

    # Time Container, Payment Vto. Section
    TC_HEIGHT = 21
    POINTER = 170
    canv.rect(LEFT_MARGIN, 170, width - LEFT_MARGIN * 2, TC_HEIGHT, stroke=1)

    # Ticket Type
    canv.setLineWidth(STRONG_STROKE)
    CONT_WIDTH = 46
    canv.setFont(BOLD_FONT, 28)

    canv.rect(width/2 - CONT_WIDTH/2, 49, CONT_WIDTH, 41, stroke=1)
    canv.drawString(width/2 - 10, 49 + 26, type)
    canv.setFont(BOLD_FONT, 7)
    canv.drawString(width/2 - 14, 49 + 37, 'COD. 011')

  # Info
    I_HEIGHT = 62
    POINTER += TC_HEIGHT + 3
    canv.rect(LEFT_MARGIN, POINTER, width -
              LEFT_MARGIN * 2, I_HEIGHT, stroke=1)


def generate_right_side_of_header(canv, pto_v, ticket_n, date, cuit, ib, ia):
    canv.setFont(BOLD_FONT, 22)
    canv.drawString(width/2 + 35, 49 + 30, 'FACTURA')

    canv.setFont(BOLD_FONT, 9)
    canv.drawString(width/2 + 35, 49 + 52,
                    f'Punto de Venta:  {pto_v}   Comp Nro:  {ticket_n}')

    canv.drawString(width/2 + 35, 49 + 64, f'Fecha de emisión:  {date}')

    canv.setFont(FONT, 9)
    canv.drawString(width/2 + 35, 49 + 88, f'CUIT:  {cuit}')
    canv.drawString(width/2 + 35, 49 + 100, f'Ingresos Brutos:  {ib}')
    canv.drawString(width/2 + 35, 49 + 112,
                    f'Fecha de Inicio de Actividades:  {ia}')


def generate_lef_side_of_header(canv, name, address):
    canv.setFont(BOLD_FONT, 22)
    canv.drawString(LEFT_MARGIN * 2, 49 + 30, name)

    canv.setFont(FONT, 9)
    canv.drawString(LEFT_MARGIN * 2, 49 + 88,
                    f'Domicilio Comercial:  {address}')
    canv.drawString(LEFT_MARGIN * 2, 49 + 64, f'Razón Social:  {name}')
    canv.setFont(BOLD_FONT, 9)
    canv.drawString(LEFT_MARGIN * 2, 49 + 112,
                    'Condición frente al IVA:  Responsable Monotributo')


def generate_date_information(canv, since, to, payment_vto):
    canv.setFont(BOLD_FONT, 10)
    HEIGHT = 184
    text_len = canv.stringWidth(
        'Período Facturado Desde:  ', BOLD_FONT, 10)

    canv.drawString(LEFT_MARGIN * 2, HEIGHT,
                    'Período Facturado Desde:  ')

    canv.setFont(FONT, 10)
    canv.drawString(LEFT_MARGIN * 2 + text_len, HEIGHT, since)

    canv.setFont(BOLD_FONT, 10)
    text_len = canv.stringWidth(
        'Hasta:  ', BOLD_FONT, 10)
    canv.drawString(LEFT_MARGIN * 2 + 210, HEIGHT,
                    'Hasta:  ')
    canv.setFont(FONT, 10)
    canv.drawString(LEFT_MARGIN * 2 + 210 +
                    text_len, HEIGHT, to)

    canv.setFont(BOLD_FONT, 10)
    text_len = canv.stringWidth(
        'Fecha de Vto. para el pago:  ', BOLD_FONT, 10)
    canv.drawString(LEFT_MARGIN * 2 + 330, HEIGHT,
                    'Fecha de Vto. para el pago:  ')
    canv.setFont(FONT, 10)
    canv.drawString(LEFT_MARGIN * 2 + 330 +
                    text_len, HEIGHT, payment_vto)


generate_page_structure(canv, 'C', 'ORIGINAL')
generate_right_side_of_header(
    canv, '0001', '0000004', '05/05/2022', '20396423295', '20396423295', '01/01/1900')
generate_lef_side_of_header(canv, 'Tomas Nocetti',
                            'Condarco 4357 - Ciudad de Buenos Aires')
generate_date_information(canv, '04/05/2022', '05/05/2022', '08/10/2022')

canv.save()
