from unittest import TestCase

from src.ticket_item import TicketItem


class TicketItemTests(TestCase):

    def test_creation(self):
        t = TicketItem(
            description='SERVICIOS WEB',
            unit_price=200,
            units=2,
            code='1'
        )
        assert(t.get_description() == 'SERVICIOS WEB')
        assert(t.get_units() == 2)
        assert(t.get_unit_price() == 200)
        assert(t.get_code() == '1')
        assert(t.get_subtotal() == 400)
