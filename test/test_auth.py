from unittest import TestCase, main, mock

from src.auth import AuthSession, ExpiredAuth
from datetime import datetime, timedelta


class AuthTest(TestCase):

    @mock.patch("src.auth.open", new_callable=mock.mock_open())
    def test_retrieve_auth_from_file_no_prev_request_raises_error(self, m):
        m.side_effect = FileNotFoundError()
        with self.assertRaises(FileNotFoundError):
            AuthSession.retrieve_auth_from_file()

    @mock.patch("src.auth.open", new_callable=mock.mock_open())
    def test_save_auth_from_file(self, m):
        token = 'DEMO'
        sign = 'SIGN'

        time = datetime.now()
        auth = AuthSession(token, sign, time)
        auth.save_auth_to_file()
        data = m().__enter__().write

        data.assert_called_once_with(
            '<authData>'
            f'<token>{token}</token>'
            f'<sign>{sign}</sign>'
            f'<expirationTime>{time.isoformat()}</expirationTime>'
            '</authData>')

    def test_retrieve_auth_from_file_raises_expired_error(self):
        delta = timedelta(minutes=20)

        time = datetime.now() - delta

        data = ('<authData>'
                f'<token>asd</token>'
                f'<sign>asd</sign>'
                f'<expirationTime>{time.isoformat()}</expirationTime>'
                '</authData>')

        m = mock.mock_open(read_data=data)
        with mock.patch('xml.etree.ElementTree.open', m):
            with self.assertRaises(ExpiredAuth):
                AuthSession.retrieve_auth_from_file()


if __name__ == "__main__":
    main()
