# tests.py
import os
from unittest import TestCase, main, mock

from src.auth import AuthSession, TMP_AUTH_RES
from datetime import datetime


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
        pass

    # @mock.patch("src.auth.")
    # def test_retrieve_auth_from_ws(self):


if __name__ == "__main__":
    main()
