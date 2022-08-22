# tests.py
from unittest import TestCase, main, mock

from src.service import AlreadyAuthenticated, solicitar_ta


class ServiceTest(TestCase):
    @mock.patch("src.service.requests.post")
    def test_success_call_auth_ws(self, mock_post):
        with open('test/responses/authResponseSuccess.xml', 'rb') as cert_file:
            response = cert_file.read()

        my_mock_response = mock.Mock(status_code=200)
        my_mock_response.content = response
        mock_post.return_value = my_mock_response  # 5

        response = solicitar_ta("payload")

        assert(
            response[0] == 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9InllcyI/Pgo8c3NvIHZlcnNpb249IjIuMCI+CiAgICA8aWQgc3JjPSJDTj13c2FhaG9tbywgTz1BRklQLCBDPUFSLCBTRVJJQUxOVU1CRVI9Q1VJVCAzMzY5MzQ1MDIzOSIgZHN0PSJDTj13c2ZlLCBPPUFGSVAsIEM9QVIiIHVuaXF1ZV9pZD0iMjM3OTI0NjA5MCIgZ2VuX3RpbWU9IjE2NjA3NjY0NDUiIGV4cF90aW1lPSIxNjYwODA5NzA1Ii8+CiAgICA8b3BlcmF0aW9uIHR5cGU9ImxvZ2luIiB2YWx1ZT0iZ3JhbnRlZCI+CiAgICAgICAgPGxvZ2luIGVudGl0eT0iMzM2OTM0NTAyMzkiIHNlcnZpY2U9IndzZmUiIHVpZD0iU0VSSUFMTlVNQkVSPUNVSVQgMjAzOTY0MjMyOTUsIENOPWZhY3R1cmFkb3J2MiIgYXV0aG1ldGhvZD0iY21zIiByZWdtZXRob2Q9IjIyIj4KICAgICAgICAgICAgPHJlbGF0aW9ucz4KICAgICAgICAgICAgICAgIDxyZWxhdGlvbiBrZXk9IjIwMzk2NDIzMjk1IiByZWx0eXBlPSI0Ii8+CiAgICAgICAgICAgIDwvcmVsYXRpb25zPgogICAgICAgIDwvbG9naW4+CiAgICA8L29wZXJhdGlvbj4KPC9zc28+Cg==')

        assert(
            response[1] == 'XPKZDOd3HGJzw088piyw335WDsVZ227jmQIHyYUnps1jTZz1IyciW3CBJddOeg1jkjZFkDTBzxT0Xgh/hyfMJpvHI3O1opTN2PaG21lpqmdMgbR+eJoKPZwcgPwO0Rbos2VeD4kgqiugUYUUa3Yagg2yeqKoTK2HbVMHZU8hfiw='
        )

    @mock.patch("src.service.requests.post")
    def test_failure_call_auth_ws_already_authenticated(self, mock_post):
        with open('test/responses/authResponseFailureAlreadyLogged.xml', 'rb') as cert_file:
            response = cert_file.read()

        my_mock_response = mock.Mock(status_code=500)
        my_mock_response.content = response
        mock_post.return_value = my_mock_response

        with self.assertRaises(AlreadyAuthenticated):
            solicitar_ta("payload")


if __name__ == "__main__":
    main()
