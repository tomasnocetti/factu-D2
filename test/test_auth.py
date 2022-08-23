from unittest import TestCase, main, mock

from src.auth import AuthSession, ExpiredAuth
from datetime import datetime, timedelta

from src.service import TaResponse


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

    def test_retrieve_auth_from_file(self):
        delta = timedelta(minutes=20)

        time = datetime.now() + delta
        token = 'TOKEN'
        sign = 'SIGN'

        data = ('<authData>'
                f'<token>{token}</token>'
                f'<sign>{sign}</sign>'
                f'<expirationTime>{time.isoformat()}</expirationTime>'
                '</authData>')

        m = mock.mock_open(read_data=data)

        with mock.patch('xml.etree.ElementTree.open', m):
            auth = AuthSession.retrieve_auth_from_file()
            assert(auth.token == token)
            assert(auth.sign == sign)
            assert(auth.expiration_time.isoformat() == time.isoformat())

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

    @mock.patch("src.auth.request_ta")
    def test_retrieve_auth_from_ws(self, m):
        res = TaResponse('TOKEN', 'SIGN', datetime.now())
        m.return_value = res
        auth = AuthSession.retrieve_auth_from_ws()

        assert(auth.token == res.get_token())
        assert(auth.sign == res.get_sign())
        assert(auth.expiration_time == res.get_expiration())


if __name__ == "__main__":
    main()
