import enum
from env import constants
from typing import List
from src.ticket_item import TicketItem
from src.ticket_recipt import TicketRecipt


class TYPE_OF_TICKET():
    PRODUCTS = 1
    SERVICES = 2


class Ticket():
    def __init__(
        self,
        emission_date,
        since,
        to,
        payment_vto,
        iva_status,
        sale,
        items: List[TicketItem],
        type_of_ticket: TYPE_OF_TICKET,
    ) -> None:
        self.emission_date = emission_date
        self.since = since
        self.to = to
        self.payment_vto = payment_vto
        self.iva_status = iva_status
        self.sale = sale
        self.items = items
        self.type_of_ticket = type_of_ticket
        self.recipt = None
        self.rec_doc_code = None
        self.rec_doc_nr = None

    def get_since(self):
        return self.since

    def get_to(self):
        return self.to

    def get_payment_vto(self):
        return self.payment_vto

    def get_iva_status(self):
        return self.iva_status

    def get_sale(self):
        return self.sale

    def get_subtotal(self):
        subtotal = 0
        for el in self.items:
            subtotal += el.get_subtotal()

        return subtotal

    def get_taxes(self):
        return 0

    def get_total(self):
        return self.get_subtotal()

    def get_recipt(self) -> TicketRecipt:
        return self.recipt

    def get_emission_date(self):
        return self.emission_date

    def set_recipt(self, recipt: TicketRecipt):
        self.recipt = recipt

    def get_items(self) -> List[TicketItem]:
        return self.items

    def set_cuit(self, cuit):
        self.rec_doc_code = constants['CUIT_DOC_CODE']
        self.rec_doc_nr = cuit

    def set_no_doc(self):
        self.rec_doc_code = constants['CONSUMIDOR_FINAL_DOC_CODE']
        self.rec_doc_nr = constants['CONSUMIDOR_FINAL_DOC_N']

    def get_rec_doc_code(self):
        return self.rec_doc_code

    def get_rec_doc_nr(self):
        return self.rec_doc_nr

    def get_type_of_ticket(self):
        return self.type_of_ticket
