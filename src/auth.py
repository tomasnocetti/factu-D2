from datetime import date, datetime, timedelta
import os
import xml.etree.ElementTree as ET

from .service import request_ta
from env import config
from .cryptography import build_cms

direct = os.path.dirname(config['TMP_AUTH_PATH'])
if (not os.path.exists(direct)):
    os.makedirs(direct)


class ExpiredAuth(Exception):
    pass


class AuthSession():
    @classmethod
    def retrieve_auth_from_file(cls):
        auth = ET.parse(config['TMP_AUTH_PATH'])
        token = auth.find('token').text
        sign = auth.find('sign').text
        expiration_time_item = datetime.fromisoformat(
            auth.find('expirationTime').text)

        current_date = datetime.today().astimezone()

        if (expiration_time_item < current_date):
            raise ExpiredAuth

        return cls(token, sign, expiration_time_item)

    @classmethod
    def retrieve_auth_from_ws(cls):
        with open(config['CERTIFICATE'], 'rb') as cert_file:
            cert_buf = cert_file.read()

        with open(config['PRIVATE_KEY'], 'rb') as key_file:
            key_buf = key_file.read()

        buffer = cls.__build_request_xml()
        cms = build_cms(cert_buf, key_buf, buffer)
        request_payload = cls.__build_ta_request(cms)

        response = request_ta(request_payload)

        return AuthSession(
            token=response.get_token(),
            sign=response.get_sign(),
            expiration_time=response.get_expiration()
        )

    @classmethod
    def init(cls):
        try:
            return cls.retrieve_auth_from_file()
        except (FileNotFoundError, ExpiredAuth):
            pass

        auth = cls.retrieve_auth_from_ws()
        auth.save_auth_to_file()
        return auth

    @classmethod
    def __build_request_xml(cls):
        solicitudXML = ET.parse('templates/solicitud.xml')

        one_minute = timedelta(minutes=1)
        generationTime = datetime.now() - one_minute
        expirationTime = datetime.now() + one_minute

        header = solicitudXML.getroot()[0]

        uniqueIdField = header[0]
        generationTimeField = header[1]
        expirationTimeField = header[2]

        uniqueIdField.text = generationTime.strftime('%y%m%d%H%M')
        generationTimeField.text = generationTime.strftime('%Y-%m-%dT%H:%M:%S')
        expirationTimeField.text = expirationTime.strftime('%Y-%m-%dT%H:%M:%S')

        return bytes(ET.tostring(solicitudXML.getroot(),
                                 encoding='unicode'), 'utf-8')

    @classmethod
    def __build_ta_request(cls, cms: str) -> str:
        mytree = ET.parse('templates/solicitudLoginCms.xml')
        myroot = mytree.getroot()

        myroot[1][0][0].text = cms

        return ET.tostring(myroot, encoding='unicode')

    def __init__(self, token, sign, expiration_time) -> None:
        self.token = token
        self.sign = sign
        self.expiration_time = expiration_time

    def save_auth_to_file(self):

        data = ET.Element('authData')
        token_item = ET.SubElement(data, 'token')
        sign_item = ET.SubElement(data, 'sign')
        expiration_time_item = ET.SubElement(data, 'expirationTime')
        token_item.text = self.token
        sign_item.text = self.sign
        expiration_time_item.text = self.expiration_time.isoformat()
        data = ET.tostring(data, encoding='unicode')

        with open(config['TMP_AUTH_PATH'], "w") as auth_file:
            auth_file.write(data)

    def generate_auth_header(self):
        return {
            'Token': self.token,
            'Sign': self.sign,
            'Cuit': config['CUIT'],
        }
