from datetime import datetime
from unittest import TestCase, mock
from src.auth import AuthSession
from src.ticket import TYPE_OF_TICKET, Ticket

from src.ticket_generator import TicketGenerator
from src.ticket_item import TicketItem
from src.user_config import UserConfig
from env import constants, cert_buf, key_buf


class TicketGeneratorTests(TestCase):

    def test_request_last_ticket_to_dev_env(self):
        user_conf = UserConfig(
            name='Asdfg',
            address='Demo 123',
            ia=datetime.now(),
            pto_v=1,
            cbe_type=constants['COD_CMP']
        )
        auth = AuthSession.init(cert_buf=cert_buf, key_buf=key_buf)

        t = TicketGenerator(
            user_conf,
            auth
        )
        assert(type(t.get_previous_ticket_n()) == int)

    def test_authorize_ticket_to_dev_env(self):
        user_conf = UserConfig(
            name='Tomas Nocetti',
            address='Calle falsa, 1234',
            ia=datetime.now(),
            pto_v=1,
            cbe_type=constants['COD_CMP']
        )
        auth = AuthSession.init(cert_buf=cert_buf, key_buf=key_buf)

        t = TicketGenerator(
            user_conf,
            auth
        )
        ticket = Ticket(
            type_of_ticket=TYPE_OF_TICKET.SERVICES,
            emission_date=datetime.now(),
            since=datetime.now(),
            to=datetime.now(),
            payment_vto=datetime.now(),
            iva_status='Consumidor Final',
            sale='Cuenta Corriente',
            items=[TicketItem('Servicios Web', 18000, 1)]
        )
        ticket.set_no_doc()

        t.authorize_ticket(ticket)
        assert(ticket.get_recipt() != None)
        assert(ticket.get_recipt().get_cae() != None)
        assert(ticket.get_recipt().get_doc_client() == ticket.get_rec_doc_nr())
