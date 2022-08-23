from datetime import datetime
import xml.etree.ElementTree as ET

TMP_AUTH_RES = 'tmp/auth.xml'


class AuthSession():
    @classmethod
    def retrieve_auth_from_file(cls):
        auth = ET.parse(TMP_AUTH_RES)
        token = auth.find('token').text
        sign = auth.find('sign').text
        expiration_time_item = datetime.fromisoformat(
            auth.find('expirationTime').text)

        return cls(token, sign, expiration_time_item)

    def __init__(self, token, sign, expirationTime) -> None:
        self.token = token
        self.sign = sign
        self.expiration_time = expirationTime

    def save_auth_to_file(self):

        data = ET.Element('authData')
        token_item = ET.SubElement(data, 'token')
        sign_item = ET.SubElement(data, 'sign')
        expiration_time_item = ET.SubElement(data, 'expirationTime')
        token_item.text = self.token
        sign_item.text = self.sign
        expiration_time_item.text = self.expiration_time.isoformat()
        data = ET.tostring(data, encoding='unicode')

        with open(TMP_AUTH_RES, "w") as auth_file:
            auth_file.write(data)
