# tests.py
import os
from unittest import TestCase, main, mock

from src.auth import AuthSession, TMP_AUTH_RES
from datetime import datetime


class AuthTest(TestCase):

    def test_retrieve_auth_from_file_no_prev_request_raises_error(self):
        if os.path.isfile(TMP_AUTH_RES):
            os.remove(TMP_AUTH_RES)

        with self.assertRaises(FileNotFoundError):
            AuthSession.retrieve_auth_from_file()

    def test_save_and_retrieve_auth_from_file(self):
        token = 'DEMO'
        sign = 'SIGN'
        time = datetime.now()

        auth = AuthSession(token, sign, time)
        auth.save_auth_to_file()

        auth_from_file = AuthSession.retrieve_auth_from_file()

        assert(auth.token == auth_from_file.token)
        assert(auth.sign == auth_from_file.sign)
        assert(auth.expiration_time.isoformat() ==
               auth_from_file.expiration_time.isoformat())


if __name__ == "__main__":
    main()
