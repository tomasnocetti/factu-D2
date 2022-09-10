from typing import List
from src.ticket_item import TicketItem
from src.ticket_recipt import TicketRecipt


class Ticket():
    def __init__(
        self,
        since,
        to,
        payment_vto,
        iva_status,
        sale,
        items: List[TicketItem]
    ) -> None:
        self.since = since
        self.to = to
        self.payment_vto = payment_vto
        self.iva_status = iva_status
        self.sale = sale
        self.items = items
        self.recipt = None

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

    def set_recipt(self, recipt: TicketRecipt):
        self.recipt = recipt

    def get_items(self) -> List[TicketItem]:
        return self.items
