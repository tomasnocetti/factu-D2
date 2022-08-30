from datetime import datetime


class TicketRecipt:
    def __init__(
        self,
        pto_v: int,
        date: datetime,
        doc_type: int,
        doc_nr: int,
        ticket_n: int,
        cae: int,
        vto_cae: datetime,
    ) -> None:
        self.pto_v = pto_v
        self.date = date
        self.doc_type = doc_type
        self.doc_nr = doc_nr
        self.ticket_n = ticket_n
        self.cae = cae
        self.vto_cae = vto_cae
