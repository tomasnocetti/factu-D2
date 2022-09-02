
from datetime import datetime
from typing import List
from reportlab.platypus import Table, TableStyle, Frame
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
import qrcode
import json
import base64

from env import constants
from src.ticket import Ticket
from src.ticket_item import TicketItem
from src.ticket_recipt import TicketRecipt
from src.user_config import UserConfig


width, height = A4  # keep for later

STROKE_COLOR = '#343434'
SROKE_WITH = 0.4
STRONG_STROKE = 0.6
STRONG_XL_STROKE = 0.8
FONT = 'Helvetica'
BOLD_FONT = 'Helvetica-Bold'
TOP_MARGIN = 21
LEFT_MARGIN = 15
HEADER_HEIGHT = 146


class PdfGenerator():
    def __init__(
        self,
        user: UserConfig,
        ticket: Ticket,
        recipt: TicketRecipt,
        items: List[TicketItem]
    ):
        self.type = 'C'
        self.user = user
        self.ticket = ticket
        self.items = items
        self.recipt = recipt
        self.canv = Canvas('doc.pdf', bottomup=1)

    def inv(self, size):
        return height - size

    def print(self):
        pages = ['ORIGINAL', 'DUPLICADO', 'TRIPLICADO']

        for page in pages:
            self.generate_page_structure(page)
            self.generate_right_side_of_header()
            self.generate_lef_side_of_header()
            self.generate_date_information()

            self.generate_items_info()
            self.generate_client_information()
            self.generate_total()
            self.generate_footer()
            self.canv.showPage()

        self.canv.save()

    def generate_page_structure(self, page_n):
        self.canv.setFont(BOLD_FONT, 22)

        self.canv.setLineWidth(SROKE_WITH)
        self.canv.setStrokeColor(STROKE_COLOR)
        self.canv.rect(LEFT_MARGIN, self.inv(TOP_MARGIN + HEADER_HEIGHT), width -
                       LEFT_MARGIN * 2, HEADER_HEIGHT, stroke=1)

        # Central divider inside header
        self.canv.line(width/2, self.inv(90), width/2, self.inv(167))

        # Horizonal divider inside header
        self.canv.setFont(BOLD_FONT, 16)
        self.canv.drawCentredString(width/2, self.inv(42), page_n)
        self.canv.line(LEFT_MARGIN, self.inv(
            49), width - LEFT_MARGIN, self.inv(49))

        # Time Container, Payment Vto. Section
        TC_HEIGHT = 21
        self.canv.rect(LEFT_MARGIN, self.inv(170 + TC_HEIGHT), width -
                       LEFT_MARGIN * 2, TC_HEIGHT, stroke=1)

        # Ticket Type
        self.canv.setLineWidth(STRONG_STROKE)
        CONT_WIDTH = 46
        self.canv.setFont(BOLD_FONT, 28)

        self.canv.rect(width/2 - CONT_WIDTH/2, self.inv(49 + 41),
                       CONT_WIDTH, 41, stroke=1)
        self.canv.drawString(width/2 - 10, self.inv(49 + 26), self.type)
        self.canv.setFont(BOLD_FONT, 7)
        self.canv.drawString(width/2 - 14, self.inv(49 + 37), 'COD. 011')

    # Info

    def generate_items_info(self):
        elements = []
        column_width = [43, 283, 65, 80, 94]
        header = ['Código', 'Producto/Servicio',
                  'Cantidad', 'Precio Unit.', 'Subtotal']

        data = [header]

        for item in self.items:
            data.append([
                item.get_code(),
                item.get_description(),
                self.f_num(item.get_units()),
                self.f_num(item.get_unit_price()),
                self.f_num(item.get_subtotal()),
            ])

        t = Table(data, colWidths=column_width)
        t.setStyle(TableStyle([('GRID', (0, 0), (7, 0), 0.5, colors.black),
                               ('TOPPADDING', (0, 0), (7, 0), 4),
                               ('BOTTOMPADDING', (0, 0), (7, 0), 4),
                               ('VALIGN', (0, 0), (7, 0), 'MIDDLE'),
                               ('BACKGROUND', (0, 0), (7, 0), colors.lightgrey)]))
        elements.append(t)
        f = Frame(LEFT_MARGIN, self.inv(260 + 200), width=width -
                  LEFT_MARGIN * 2, height=200)
        f.addFromList(elements, self.canv)

    def generate_right_side_of_header(self):
        self.canv.setFont(BOLD_FONT, 22)
        self.canv.drawString(width/2 + 35, self.inv(49 + 30), 'FACTURA')

        self.canv.setFont(BOLD_FONT, 9)
        str_pto_v = str(self.recipt.get_pto_v())
        str_ticket_n = str(self.recipt.get_ticket_n())

        len_pto_v = len(str_pto_v)
        len_ticket_n = len(str_ticket_n)

        self.canv.drawString(width/2 + 35, self.inv(49 + 52),
                             f'Punto de Venta:  {str_pto_v.zfill(6 - len_pto_v)}   Comp Nro:  {str_ticket_n.zfill(9 - len_ticket_n)}')

        self.canv.drawString(width/2 + 35, self.inv(49 + 64),
                             f'Fecha de emisión:  {self.recipt.get_date().strftime("%d/%m/%Y")}')

        self.canv.setFont(FONT, 9)
        self.canv.drawString(
            width/2 + 35, self.inv(49 + 88), f'Doc.:  {self.recipt.get_cuit()}')
        self.canv.drawString(width/2 + 35, self.inv(49 + 100),
                             f'Ingresos Brutos:  {self.recipt.get_cuit()}')
        self.canv.drawString(width/2 + 35, self.inv(49 + 112),
                             f'Fecha de Inicio de Actividades:  {self.user.get_ia().strftime("%d/%m/%Y")}')

    def generate_lef_side_of_header(self):
        BASE = 49
        self.canv.setFont(BOLD_FONT, 22)
        self.canv.drawString(
            LEFT_MARGIN * 2, self.inv(BASE + 30), self.user.get_name())

        self.canv.setFont(FONT, 9)
        self.canv.drawString(LEFT_MARGIN * 2, self.inv(BASE + 88),
                             f'Domicilio Comercial:  {self.user.get_address()}')
        self.canv.drawString(LEFT_MARGIN * 2, self.inv(BASE + 64),
                             f'Razón Social:  {self.user.get_name()}')
        self.canv.setFont(BOLD_FONT, 9)
        self.canv.drawString(LEFT_MARGIN * 2, self.inv(BASE + 112),
                             'Condición frente al IVA:  Responsable Monotributo')

    def generate_date_information(self):
        self.canv.setFont(BOLD_FONT, 10)
        HEIGHT = 184
        text_len = self.canv.stringWidth(
            'Período Facturado Desde:  ', BOLD_FONT, 10)

        self.canv.drawString(LEFT_MARGIN * 2, self.inv(HEIGHT),
                             'Período Facturado Desde:  ')

        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + text_len,
                             self.inv(HEIGHT), self.ticket.get_since().strftime("%d/%m/%Y"))

        self.canv.setFont(BOLD_FONT, 10)
        text_len = self.canv.stringWidth(
            'Hasta:  ', BOLD_FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 210, self.inv(HEIGHT),
                             'Hasta:  ')
        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 210 +
                             text_len, self.inv(HEIGHT), self.ticket.get_to().strftime("%d/%m/%Y"))

        self.canv.setFont(BOLD_FONT, 10)
        text_len = self.canv.stringWidth(
            'Fecha de Vto. para el pago:  ', BOLD_FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 330, self.inv(HEIGHT),
                             'Fecha de Vto. para el pago:  ')
        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 330 +
                             text_len, self.inv(HEIGHT), self.ticket.get_payment_vto().strftime("%d/%m/%Y"))

    def generate_client_information(self):
        POINTER = 194
        I_HEIGHT = 62
        PADDING = 15
        self.canv.rect(LEFT_MARGIN, self.inv(POINTER + I_HEIGHT), width -
                       LEFT_MARGIN * 2, I_HEIGHT, stroke=1)

        self.canv.setFont(BOLD_FONT, 9)

        self.canv.drawString(LEFT_MARGIN * 2, self.inv(POINTER +
                             PADDING), f'CUIT: {self.recipt.get_doc_client()}')

        self.canv.drawString(LEFT_MARGIN * 2, self.inv(POINTER + PADDING * 2 + 4),
                             f'Condición frente al IVA:   {self.ticket.get_iva_status()}')

        self.canv.drawString(LEFT_MARGIN * 2, self.inv(POINTER + PADDING * 3 + 9),
                             f'Condición de venta:   {self.ticket.get_sale()}')

    def generate_total(self):
        POINTER = 580
        I_HEIGHT = 94
        PADDING = 20
        self.canv.setFont(BOLD_FONT, 10)
        self.canv.setLineWidth(STRONG_XL_STROKE)
        self.canv.rect(LEFT_MARGIN, self.inv(POINTER + I_HEIGHT), width -
                       LEFT_MARGIN * 2, I_HEIGHT, stroke=1)

        POINTER = 600
        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, self.inv(POINTER +
                                  PADDING), 'Subtotal: $')

        self.canv.drawRightString(width - LEFT_MARGIN * 2, self.inv(POINTER +
                                  PADDING), self.f_num(self.ticket.get_subtotal()))

        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, self.inv(POINTER + PADDING * 2),
                                  'Importe Otros Tributos: $')

        self.canv.drawRightString(width - LEFT_MARGIN * 2, self.inv(POINTER +
                                  PADDING * 2 + 4), self.f_num(self.ticket.get_taxes()))
        self.canv.setFont(BOLD_FONT, 11)
        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, self.inv(POINTER + PADDING * 3),
                                  'Importe Total: $')

        self.canv.drawRightString(width - LEFT_MARGIN * 2, self.inv(POINTER + PADDING * 3),
                                  self.f_num(self.ticket.get_total()))

    def f_num(self, num: float):
        return "{:.2f}".format(num).replace(".", ",")

    def generate_footer(self):
        POINTER = 684
        PADDING = 10

        data = {
            "ver": 1,
            "fecha": self.recipt.get_date().strftime("%Y-%m-%d"),
            "cuit": self.recipt.get_cuit(),
            "ptoVta": self.recipt.get_pto_v(),
            "tipoCmp": self.recipt.get_ticket_code(),
            "nroCmp": self.recipt.get_ticket_n(),
            "importe": self.ticket.get_total(),
            "moneda": "PES",
            "ctz": 1,
            "tipoCodAut": "E",
            "codAut": self.recipt.get_cae()
        }

        json_data = json.dumps(data)
        base64_data = base64.b64encode(
            json_data.encode('ascii')).decode('ascii')

        url = constants['BASE_QR_URL'] + base64_data
        img = qrcode.make(url)

        self.canv.drawCentredString(
            width/2, self.inv(POINTER + PADDING), f'Pág. 1/1')
        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, self.inv(POINTER + PADDING),
                                  'CAE N:')

        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, self.inv(POINTER + PADDING * 3),
                                  'Fecha de Vto. de CAE:')

        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + width * 3/4 + 10, self.inv(POINTER + PADDING),
                             str(self.recipt.get_cae()))
        self.canv.drawString(LEFT_MARGIN * 2 + width * 3/4 + 10, self.inv(POINTER + PADDING * 3),
                             self.recipt.get_vto_cae().strftime("%d/%m/%Y"))

        self.canv.drawInlineImage(img, LEFT_MARGIN * 2,
                                  self.inv(POINTER + 90), width=90, height=90)

        self.canv.drawImage('assets/afip_img.png', LEFT_MARGIN * 2 + 100,
                            self.inv(POINTER + 20 + 45), height=45, width=100)


a = PdfGenerator(
    user=UserConfig(
        name='Tomas Nocetti',
        address='Siempre Viva 123, CABA',
        ia=datetime.now()
    ),
    ticket=Ticket(
        since=datetime.now(),
        to=datetime.now(),
        payment_vto=datetime.now(),
        iva_status='Consumidor Final',
        sale='Cuenta Corriente',
        subtotal=280.10,
        taxes=0,
        total=280.10
    ),
    recipt=TicketRecipt(
        ticket_code=11,
        pto_v=1,
        date=datetime.now(),
        cuit=20396423295,
        doc_type=99,
        doc=0,
        ticket_n=4,
        cae=4512302131,
        vto_cae=datetime.now()
    ),
    items=[TicketItem('Servicios Web', 18000, 1)])

a.print()
