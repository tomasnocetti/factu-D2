from datetime import datetime


class Ticket():
    def __init__(
        self,
    ) -> None:
        self.since = datetime.now()
        self.to = datetime.now()
        self.payment_vto = datetime.now()
        self.iva_status = 'Consumidor Final'
        self.sale = 'Cuenta Corriente'
        self.subtotal = 280.10
        self.taxes = 0
        self.total = 280.10

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
