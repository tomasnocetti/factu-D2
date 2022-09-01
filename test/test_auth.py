from unittest import TestCase, main, mock

from src.auth import AuthSession, ExpiredAuth
from datetime import date, datetime, timedelta

from src.service import TaResponse

delta = timedelta(minutes=20)

valid_time = datetime.now().astimezone() + delta
invalid_time = datetime.now().astimezone() - delta


class AuthTest(TestCase):

    @mock.patch("xml.etree.ElementTree.open", new_callable=mock.mock_open())
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

        token = 'TOKEN'
        sign = 'SIGN'

        data = ('<authData>'
                f'<token>{token}</token>'
                f'<sign>{sign}</sign>'
                f'<expirationTime>{valid_time.isoformat()}</expirationTime>'
                '</authData>')

        m = mock.mock_open(read_data=data)

        with mock.patch('xml.etree.ElementTree.open', m):
            auth = AuthSession.retrieve_auth_from_file()
            assert(auth.token == token)
            assert(auth.sign == sign)
            assert(auth.expiration_time.isoformat() == valid_time.isoformat())

    def test_retrieve_auth_from_file_raises_expired_error(self):

        data = ('<authData>'
                f'<token>asd</token>'
                f'<sign>asd</sign>'
                f'<expirationTime>{invalid_time.isoformat()}</expirationTime>'
                '</authData>')

        m = mock.mock_open(read_data=data)
        with mock.patch('xml.etree.ElementTree.open', m):
            with self.assertRaises(ExpiredAuth):
                AuthSession.retrieve_auth_from_file()

    @mock.patch("src.auth.open", new_callable=mock.mock_open())
    @mock.patch("src.auth.request_ta")
    def test_retrieve_auth_from_ws(self, m, m_open):
        res = TaResponse('TOKEN', 'SIGN', datetime.now())
        m.return_value = res

        with open('test/credentials/certificado.pem', 'rb') as cert_file:
            cert_buf = cert_file.read()

        with open('test/credentials/clave.key', 'rb') as key_file:
            key_buf = key_file.read()

        m_open().__enter__().read.side_effect = [cert_buf, key_buf]
        auth = AuthSession.retrieve_auth_from_ws()

        assert(auth.token == res.get_token())
        assert(auth.sign == res.get_sign())
        assert(auth.expiration_time == res.get_expiration())

    @mock.patch("src.auth.AuthSession.retrieve_auth_from_file")
    def test_init_auth_from_file(self, m):

        token = 'TOKEN'
        sign = 'SIGN'
        m.return_value = AuthSession(
            token=token, sign=sign, expiration_time=valid_time)

        auth = AuthSession.init()

        assert(auth.token == token)
        assert(auth.sign == sign)
        assert(auth.expiration_time.isoformat() == valid_time.isoformat())

    @mock.patch("src.auth.AuthSession.retrieve_auth_from_ws")
    @mock.patch("src.auth.AuthSession.retrieve_auth_from_file")
    def test_init_auth_from_ws_due_to_file_nfound(self, mfile, mws):
        mfile.side_effect = FileNotFoundError

        token = 'TOKEN'
        sign = 'SIGN'
        mws.return_value = AuthSession(
            token=token, sign=sign, expiration_time=valid_time)

        auth = AuthSession.init()

        assert(auth.token == token)
        assert(auth.sign == sign)
        assert(auth.expiration_time.isoformat() == valid_time.isoformat())

    @mock.patch("src.auth.AuthSession.retrieve_auth_from_ws")
    @mock.patch("src.auth.AuthSession.retrieve_auth_from_file")
    def test_init_auth_from_ws_due_to_file_expiredauth(self, mfile, mws):
        mfile.side_effect = ExpiredAuth

        token = 'TOKEN'
        sign = 'SIGN'
        mws.return_value = AuthSession(
            token=token, sign=sign, expiration_time=valid_time)

        auth = AuthSession.init()

        assert(auth.token == token)
        assert(auth.sign == sign)
        assert(auth.expiration_time.isoformat() == valid_time.isoformat())

    @mock.patch("src.auth.AuthSession.save_auth_to_file")
    @mock.patch("src.auth.AuthSession.retrieve_auth_from_ws")
    @mock.patch("src.auth.AuthSession.retrieve_auth_from_file")
    def test_init_auth_from_ws_persists_info(self, mfile, mws, msaf):
        mfile.side_effect = ExpiredAuth

        token = 'TOKEN'
        sign = 'SIGN'
        mws.return_value = AuthSession(
            token=token, sign=sign, expiration_time=valid_time)

        AuthSession.init()

        msaf.assert_called_once()


if __name__ == "__main__":
    main()
