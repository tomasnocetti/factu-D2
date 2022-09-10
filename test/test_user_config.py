from datetime import datetime
from unittest import TestCase

from src.user_config import UserConfig
from env import constants


class TicketItemTests(TestCase):

    def test_creation(self):
        date = datetime.now()
        address = 'Calle Viva 123, CABA'
        t = UserConfig(
            name='Tomas Nocetti',
            address=address,
            ia=date,
            pto_v=1,
            cbe_type=constants['COD_CMP']
        )

        assert(t.get_address() == address)
        assert(t.get_name() == 'Tomas Nocetti')
        assert(t.get_ia() == date)
        assert(t.get_pto_vta() == 1)
