from datetime import datetime, timedelta
from unittest import TestCase

from src.ticket_item import TicketItem
from src.ticket import TYPE_OF_TICKET, Ticket
from env import constants

emitted = datetime.now()
since = datetime.now() + timedelta(minutes=10)
to = datetime.now() + timedelta(minutes=20)
payment_vto = datetime.now() + timedelta(minutes=40)


class TicketTests(TestCase):

    def test_creation(self):
        t = Ticket(
            emission_date=emitted,
            type_of_ticket=TYPE_OF_TICKET.SERVICES,
            since=since,
            to=to,
            payment_vto=payment_vto,
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1),
                   TicketItem('Servicios Web', 10000, 1)]
        )
        assert(t.get_type_of_ticket() == TYPE_OF_TICKET.SERVICES)
        assert(t.get_since() == since)
        assert(t.get_to() == to)
        assert(t.get_payment_vto() == payment_vto)
        assert(t.get_total() == 28000)
        assert(t.get_subtotal() == 28000)
        assert(t.get_taxes() == 0)
        assert(t.get_emission_date() == emitted)

    def test_get_recipt_for_not_authorized_ticket(self):
        t = Ticket(
            emission_date=emitted,
            type_of_ticket=TYPE_OF_TICKET.SERVICES,
            since=since,
            to=to,
            payment_vto=payment_vto,
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1),
                   TicketItem('Servicios Web', 10000, 1)]
        )
        assert(t.get_recipt() == None)

    def test_set_cuit(self):
        t = Ticket(
            emission_date=emitted,
            type_of_ticket=TYPE_OF_TICKET.SERVICES,
            since=since,
            to=to,
            payment_vto=payment_vto,
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1),
                   TicketItem('Servicios Web', 10000, 1)]
        )

        t.set_cuit(20392129301)
        assert(t.get_rec_doc_code() == constants['CUIT_DOC_CODE'])

    def test_set_final_consumer(self):
        t = Ticket(
            emission_date=emitted,
            since=since,
            type_of_ticket=TYPE_OF_TICKET.SERVICES,
            to=to,
            payment_vto=payment_vto,
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1),
                   TicketItem('Servicios Web', 10000, 1)]
        )

        t.set_no_doc()
        assert(t.get_rec_doc_code() == constants['CONSUMIDOR_FINAL_DOC_CODE'])
