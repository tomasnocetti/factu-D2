import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from env import config


class AlreadyAuthenticated(Exception):
    ERROR = 'coe.alreadyAuthenticated'
    pass


class TaResponse:
    def __init__(self, token, sign, expiration) -> None:
        self._token = token
        self._sign = sign
        self._expiration = expiration

    def get_token(self):
        return self._token

    def get_sign(self):
        return self._sign

    def get_expiration(self):
        return self._expiration


def request_ta(payload: str) -> TaResponse:

    headers = {'content-type': 'text/xml',
               'charset': 'utf-8', 'SOAPAction': 'urn:LoginCms'}

    response = requests.post(config['AUTH_URL'], data=payload, headers=headers)

    content = response.content.decode('UTF-8')
    xml_response = ET.fromstring(content)

    if(response.status_code == 500):
        fault_element = xml_response[0][0]
        fault_code = fault_element.find('faultcode').text
        fault_string = fault_element.find('faultstring').text

        if(AlreadyAuthenticated.ERROR in fault_code):
            raise AlreadyAuthenticated
        else:
            raise Exception(f'code: {fault_code} \n msg: {fault_string}')

    loginCMSReturn = xml_response[0][0][0]

    loginCMSReturnXML = ET.fromstring(loginCMSReturn.text)

    header = loginCMSReturnXML.find('header')
    expirationDate = datetime.fromisoformat(header.find('expirationTime').text)

    credentials = loginCMSReturnXML.find('credentials')
    token = credentials.find('token').text
    sign = credentials.find('sign').text

    return TaResponse(token, sign, expirationDate)
