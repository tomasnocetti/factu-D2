from datetime import datetime


class Ticket():
    def __init__(
        self,
        since,
        to,
        payment_vto,
        iva_status,
        sale,
        subtotal,
        taxes,
        total
    ) -> None:
        self.since = since
        self.to = to
        self.payment_vto = payment_vto
        self.iva_status = iva_status
        self.sale = sale
        self.subtotal = subtotal
        self.taxes = taxes
        self.total = total

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
        return self.subtotal

    def get_taxes(self):
        return self.taxes

    def get_total(self):
        return self.total
