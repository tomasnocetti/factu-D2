from cgitb import text
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import qrcode
from reportlab.pdfgen.canvas import Canvas


width, height = A4  # keep for later

styleSheet = getSampleStyleSheet()
style = styleSheet['BodyText']

canv = Canvas('doc.pdf', bottomup=0)

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
        pto_v,
        ticket_n,
        date,
        cuit,
        ib,
        ia,
        name,
        address,
        since,
        to,
        payment_vto,
        doc,
        iva_status,
        sale,
        subtotal,
        taxes,
        total,
        qrdata,
        cae,
        vto_cae
    ):
        self.type = 'C'
        self.ticket_n = ticket_n
        self.pto_v = pto_v
        self.date = date
        self.cuit = cuit
        self.name = name
        self.address = address
        self.ib = ib
        self.ia = ia
        self.since = since
        self.to = to
        self.payment_vto = payment_vto
        self.doc = doc
        self.iva_status = iva_status
        self.sale = sale
        self.subtotal = subtotal
        self.taxes = taxes
        self.total = total
        self.qrdata = qrdata
        self.cae = cae
        self.vto_cae = vto_cae

        self.canv = Canvas('doc.pdf', bottomup=0)

    def print(self):
        pages = ['ORIGINAL', 'DUPLICADO', 'TRIPLICADO']

        for page in pages:
            self.generate_page_structure(page)
            self.generate_right_side_of_header()
            self.generate_lef_side_of_header()
            self.generate_date_information()

            self.generate_client_information()
            self.generate_total()
            self.generate_footer()
            self.canv.showPage()

        self.canv.save()

    def generate_page_structure(self, page_n):
        self.canv.setFont(BOLD_FONT, 22)

        self.canv.setLineWidth(SROKE_WITH)
        self.canv.setStrokeColor(STROKE_COLOR)
        self.canv.rect(LEFT_MARGIN, TOP_MARGIN, width -
                       LEFT_MARGIN * 2, HEADER_HEIGHT, stroke=1)

        # Central divider inside header
        self.canv.line(width/2, 90, width/2, 167)

        # Horizonal divider inside header
        self.canv.setFont(BOLD_FONT, 16)
        self.canv.drawCentredString(width/2, 42, page_n)
        self.canv.line(LEFT_MARGIN, 49, width - LEFT_MARGIN, 49)

        # Time Container, Payment Vto. Section
        TC_HEIGHT = 21
        self.canv.rect(LEFT_MARGIN, 170, width -
                       LEFT_MARGIN * 2, TC_HEIGHT, stroke=1)

        # Ticket Type
        self.canv.setLineWidth(STRONG_STROKE)
        CONT_WIDTH = 46
        self.canv.setFont(BOLD_FONT, 28)

        self.canv.rect(width/2 - CONT_WIDTH/2, 49, CONT_WIDTH, 41, stroke=1)
        self.canv.drawString(width/2 - 10, 49 + 26, self.type)
        self.canv.setFont(BOLD_FONT, 7)
        self.canv.drawString(width/2 - 14, 49 + 37, 'COD. 011')

    # Info

    def generate_right_side_of_header(self):
        self.canv.setFont(BOLD_FONT, 22)
        self.canv.drawString(width/2 + 35, 49 + 30, 'FACTURA')

        self.canv.setFont(BOLD_FONT, 9)
        self.canv.drawString(width/2 + 35, 49 + 52,
                             f'Punto de Venta:  {self.pto_v}   Comp Nro:  {self.ticket_n}')

        self.canv.drawString(width/2 + 35, 49 + 64,
                             f'Fecha de emisión:  {self.date}')

        self.canv.setFont(FONT, 9)
        self.canv.drawString(width/2 + 35, 49 + 88, f'Doc.:  {self.cuit}')
        self.canv.drawString(width/2 + 35, 49 + 100,
                             f'Ingresos Brutos:  {self.ib}')
        self.canv.drawString(width/2 + 35, 49 + 112,
                             f'Fecha de Inicio de Actividades:  {self.ia}')

    def generate_lef_side_of_header(self):
        self.canv.setFont(BOLD_FONT, 22)
        self.canv.drawString(LEFT_MARGIN * 2, 49 + 30, self.name)

        self.canv.setFont(FONT, 9)
        self.canv.drawString(LEFT_MARGIN * 2, 49 + 88,
                             f'Domicilio Comercial:  {self.address}')
        self.canv.drawString(LEFT_MARGIN * 2, 49 + 64,
                             f'Razón Social:  {self.name}')
        self.canv.setFont(BOLD_FONT, 9)
        self.canv.drawString(LEFT_MARGIN * 2, 49 + 112,
                             'Condición frente al IVA:  Responsable Monotributo')

    def generate_date_information(self):
        self.canv.setFont(BOLD_FONT, 10)
        HEIGHT = 184
        text_len = canv.stringWidth(
            'Período Facturado Desde:  ', BOLD_FONT, 10)

        self.canv.drawString(LEFT_MARGIN * 2, HEIGHT,
                             'Período Facturado Desde:  ')

        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + text_len, HEIGHT, self.since)

        self.canv.setFont(BOLD_FONT, 10)
        text_len = canv.stringWidth(
            'Hasta:  ', BOLD_FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 210, HEIGHT,
                             'Hasta:  ')
        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 210 +
                             text_len, HEIGHT, self.to)

        self.canv.setFont(BOLD_FONT, 10)
        text_len = canv.stringWidth(
            'Fecha de Vto. para el pago:  ', BOLD_FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 330, HEIGHT,
                             'Fecha de Vto. para el pago:  ')
        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + 330 +
                             text_len, HEIGHT, self.payment_vto)

    def generate_client_information(self):
        POINTER = 194
        I_HEIGHT = 62
        PADDING = 15
        self.canv.rect(LEFT_MARGIN, 194, width -
                       LEFT_MARGIN * 2, I_HEIGHT, stroke=1)

        self.canv.setFont(BOLD_FONT, 9)

        self.canv.drawString(LEFT_MARGIN * 2, POINTER +
                             PADDING, f'CUIT: {self.doc}')

        self.canv.drawString(LEFT_MARGIN * 2, POINTER + PADDING * 2 + 4,
                             f'Condición frente al IVA:   {self.iva_status}')

        self.canv.drawString(LEFT_MARGIN * 2, POINTER + PADDING * 3 + 9,
                             f'Condición de venta:   {self.sale}')

    def generate_total(self):
        POINTER = 580
        I_HEIGHT = 94
        PADDING = 20
        self.canv.setFont(BOLD_FONT, 10)
        self.canv.setLineWidth(STRONG_XL_STROKE)
        self.canv.rect(LEFT_MARGIN, POINTER, width -
                       LEFT_MARGIN * 2, I_HEIGHT, stroke=1)

        POINTER = 600
        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, POINTER +
                                  PADDING, 'Subtotal: $')

        self.canv.drawRightString(width - LEFT_MARGIN * 2, POINTER +
                                  PADDING, self.subtotal)

        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, POINTER + PADDING * 2,
                                  'Importe Otros Tributos: $')

        self.canv.drawRightString(width - LEFT_MARGIN * 2, POINTER +
                                  PADDING * 2 + 4, self.taxes)
        self.canv.setFont(BOLD_FONT, 11)
        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, POINTER + PADDING * 3,
                                  'Importe Total: $')

        self.canv.drawRightString(width - LEFT_MARGIN * 2, POINTER + PADDING * 3,
                                  self.total)

    def generate_footer(self):
        POINTER = 684
        PADDING = 10

        img = qrcode.make(self.qrdata)
        self.canv.drawCentredString(width/2, POINTER + PADDING, f'Pág. 1/1')
        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, POINTER + PADDING,
                                  'CAE N:')

        self.canv.drawRightString(LEFT_MARGIN * 2 + width * 3/4, POINTER + PADDING * 3,
                                  'Fecha de Vto. de CAE:')

        self.canv.setFont(FONT, 10)
        self.canv.drawString(LEFT_MARGIN * 2 + width * 3/4 + 10, POINTER + PADDING,
                             self.cae)
        self.canv.drawString(LEFT_MARGIN * 2 + width * 3/4 + 10, POINTER + PADDING * 3,
                             self.vto_cae)

        self.canv.drawInlineImage(img, LEFT_MARGIN * 2,
                                  POINTER - 90, width=90, height=90)

        self.canv.drawImage('assets/afip_img.png', LEFT_MARGIN * 2 + 100,
                            POINTER + 20, height=45, width=100)


a = PdfGenerator('0001', '0000004', '05/05/2022', '20396423295', '20396423295', '01/01/1900', 'Tomas Nocetti',
                 'Condarco 4357 - Ciudad de Buenos Aires', '04/05/2022', '05/05/2022', '08/10/2022', '0', 'Consumidor Final', 'Cuenta Corriente', '280', '0', '280', 'https://www.afip.gob.ar/fe/qr/?p=eyJ2ZXIiOjEsImZlY2hhIjoiMjAyMi0wNS0yOSIsImN1aXQiOjIwMzk2NDIzMjk1LCJwdG9WdGEiOjEsInRpcG9DbXAiOjExLCJucm9DbXAiOjY5LCJpbXBvcnRlIjo1MDI1LCJtb25lZGEiOiJQRVMiLCJjdHoiOjEsInRpcG9Db2RBdXQiOiJFIiwiY29kQXV0Ijo3MjIyNTg4NDIzNzE4OX0=', '23023020311111', '08/06/2022')

a.print()
