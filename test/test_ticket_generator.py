from datetime import datetime
from unittest import TestCase, mock
from src.auth import AuthSession
from src.ticket import Ticket

from src.ticket_generator import TicketGenerator
from src.user_config import UserConfig
from env import constants


class TicketGeneratorTests(TestCase):

    @mock.patch('src.ticket_generator.request_last_ticket_emitted')
    def test_creation(self, m):
        m.return_value = 4

        user_conf = UserConfig(
            name='Asdfg',
            address='Demo 123',
            ia=datetime.now(),
            pto_v=1,
            cbe_type=constants['COD_CMP']
        )
        token = 'DEMO'
        sign = 'SIGN'

        time = datetime.now()
        auth = AuthSession(token, sign, time)

        t = TicketGenerator(
            user_conf,
            auth
        )
        assert(t.get_previous_ticket_n() == 4)
        m.assert_called_with(
            auth.generate_auth_header(), user_conf.get_pto_vta())
