from datetime import datetime, timedelta
from unittest import TestCase

from src.ticket_item import TicketItem
from src.ticket import Ticket


since = datetime.now()
to = datetime.now() + timedelta(minutes=20)
payment_vto = datetime.now() + timedelta(minutes=40)


class TicketTests(TestCase):

    def test_creation(self):
        t = Ticket(
            since=since,
            to=to,
            payment_vto=payment_vto,
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1),
                   TicketItem('Servicios Web', 10000, 1)]
        )
        assert(t.get_since() == since)
        assert(t.get_to() == to)
        assert(t.get_payment_vto() == payment_vto)
        assert(t.get_total() == 28000)
        assert(t.get_subtotal() == 28000)
        assert(t.get_taxes() == 0)

    def test_get_recipt_for_not_authorized_ticket(self):
        t = Ticket(
            since=since,
            to=to,
            payment_vto=payment_vto,
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1),
                   TicketItem('Servicios Web', 10000, 1)]
        )
        assert(t.get_recipt() == None)
