from datetime import datetime


class TicketRecipt:
    def __init__(
        self,
        ticket_code: int,
        pto_v: int,
        date: datetime,
        cuit: int,
        doc_type: int,
        doc: int,
        ticket_n: int,
        cae: int,
        vto_cae: datetime,
    ) -> None:
        self.pto_v = pto_v
        self.date = date
        self.doc_type = doc_type
        self.doc_client = doc
        self.ticket_n = ticket_n
        self.cae = cae
        self.vto_cae = vto_cae
        self.cuit = cuit
        self.ticket_code = ticket_code

    def get_pto_v(self):
        return self.pto_v

    def get_date(self):
        return self.date

    def get_doc_client(self):
        return self.doc_client

    def get_doc_type(self):
        return self.doc_type

    def get_doc_client(self):
        return self.doc_client

    def get_ticket_n(self):
        return self.ticket_n

    def get_cae(self):
        return self.cae

    def get_vto_cae(self):
        return self.vto_cae

    def get_cuit(self):
        return self.cuit

    def get_ticket_code(self):
        return self.ticket_code
