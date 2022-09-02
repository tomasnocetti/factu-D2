from datetime import datetime
from unittest import TestCase

from src.user_config import UserConfig


class TicketItemTests(TestCase):

    def test_creation(self):
        date = datetime.now()
        address = 'Calle Viva 123, CABA'
        t = UserConfig(
            name='Tomas Nocetti',
            address=address,
            ia=date
        )

        assert(t.get_address() == address)
        assert(t.get_name() == 'Tomas Nocetti')
        assert(t.get_ia() == date)
