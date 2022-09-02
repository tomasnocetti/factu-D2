# tests.py
import json
from unittest import TestCase, main, mock

from src.service import AlreadyAuthenticated, request_ta, request_last_ticket_emitted, request_ticket
from src.ticket_recipt import TicketRecipt


class ServiceTest(TestCase):
    @mock.patch("src.service.requests.post")
    def test_success_call_auth_ws(self, mock_post):
        with open('test/responses/authResponseSuccess.xml', 'rb') as cert_file:
            response = cert_file.read()

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = response
        mock_post.return_value = my_mock_response  # 5

        response = request_ta("payload")

        assert(
            response.get_token() == 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/Pgo8c3NvIHZlcnNpb249IjIuMCI+CiAgICA8aWQgc3JjPSJDTj13c2FhaG9tbywgTz1BRklQLCBDPUFSLCBTRVJJQUxOVU1CRVI9Q1VJVCAzMzY5MzQ1MDIzOSIgZHN0PSJDTj13c2ZlLCBPPUFGSVAsIEM9QVIiIHVuaXF1ZV9pZD0iMjM3OTI0NjA5MCIgZ2VuX3RpbWU9IjE2NjA3NjY0NDUiIGV4cF90aW1lPSIxNjYwODA5NzA1Ii8+CiAgICA8b3BlcmF0aW9uIHR5cGU9ImxvZ2luIiB2YWx1ZT0iZ3JhbnRlZCI+CiAgICAgICAgPGxvZ2luIGVudGl0eT0iMzM2OTM0NTAyMzkiIHNlcnZpY2U9IndzZmUiIHVpZD0iU0VSSUFMTlVNQkVSPUNVSVQgMjAzOTY0MjMyOTUsIENOPWZhY3R1cmFkb3J2MiIgYXV0aG1ldGhvZD0iY21zIiByZWdtZXRob2Q9IjIyIj4KICAgICAgICAgICAgPHJlbGF0aW9ucz4KICAgICAgICAgICAgICAgIDxyZWxhdGlvbiBrZXk9IjIwMzk2NDIzMjk1IiByZWx0eXBlPSI0Ii8+CiAgICAgICAgICAgIDwvcmVsYXRpb25zPgogICAgICAgIDwvbG9naW4+CiAgICA8L29wZXJhdGlvbj4KPC9zc28+Cg==')

        assert(
            response.get_sign() == 'XPKZDOd3HGJzw088piyw335WDsVZ227jmQIHyYUnps1jTZz1IyciW3CBJddOeg1jkjZFkDTBzxT0Xgh/hyfMJpvHI3O1opTN2PaG21lpqmdMgbR+eJoKPZwcgPwO0Rbos2VeD4kgqiugUYUUa3Yagg2yeqKoTK2HbVMHZU8hfiw='
        )

    @mock.patch("src.service.requests.post")
    def test_failure_call_auth_ws_already_authenticated(self, mock_post):
        with open('test/responses/authResponseFailureAlreadyLogged.xml', 'rb') as cert_file:
            response = cert_file.read()

        my_mock_response = mock.Mock(status_code=500)
        my_mock_response.content = response
        mock_post.return_value = my_mock_response

        with self.assertRaises(AlreadyAuthenticated):
            request_ta("payload")

    @mock.patch('src.service.client')
    def test_success_call_last_ticket_ws(self, wsdl_mock):
        with open('test/responses/lastTicketResponseSuccess.json', 'r') as file:
            response = json.load(file)

        mock_client = mock.Mock(return_value=response)

        wsdl_mock.service.FECompUltimoAutorizado = mock_client

        auth_header = {
            'demo': 'auth'
        }
        res = request_last_ticket_emitted(auth_header, 11)

        assert(int(response['CbteNro']) == res)
        wsdl_mock.service.FECompUltimoAutorizado.assert_called_once()

    @mock.patch('src.service.client')
    def test_success_call_ticket_ws(self, wsdl_mock):
        with open('test/responses/ticketResponseSuccess.json', 'r') as file:
            response = json.load(file)

        mock_client = mock.Mock(return_value=response)

        wsdl_mock.service.FECAESolicitar = mock_client

        auth_header = {
            'demo': 'auth'
        }

        payload = {}

        res = request_ticket(auth_header, payload)

        self.assertIsInstance(res, TicketRecipt)

    @mock.patch('src.service.client')
    def test_failure_call_ticket_ws_code_10016(self, wsdl_mock):

        with open('test/responses/ticketResponseFailureCode10016.json', 'r') as file:
            response = json.load(file)

        mock_client = mock.Mock(return_value=response)

        wsdl_mock.service.FECAESolicitar = mock_client

        auth_header = {
            'demo': 'auth'
        }

        payload = {}

        with self.assertRaises(Exception) as exc:
            request_ticket(auth_header, payload)


if __name__ == "__main__":
    main()
