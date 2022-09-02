import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from env import config, constants
from zeep import Client
from .ticket_recipt import TicketRecipt

client = Client(config['FACTURACION_WSDL'])


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


def request_ticket(auth: dict, req: dict) -> TicketRecipt:

    res = client.service.FECAESolicitar(
        Auth=auth,
        FeCAEReq=req
    )
    errors = res['Errors']

    if (errors is not None):
        err = errors['Err'][0]
        raise Exception(f'code: {err["Code"]} \n msg: {err["Msg"]}')

    cab_res = res['FeCabResp']
    der_res = res['FeDetResp']
    res = der_res['FECAEDetResponse'][0]

    return TicketRecipt(
        cuit=cab_res['Cuit'],
        pto_v=cab_res['PtoVta'],
        date=datetime.strptime(res['CbteFch'], '%Y%m%d'),
        doc=res['DocNro'],
        cae=res['CAE'],
        vto_cae=datetime.strptime(res['CAEFchVto'], '%Y%m%d'),
        ticket_n=res['CbteDesde'],
        doc_type=res['DocTipo']
    )


def request_last_ticket_emitted(auth: dict, pto_v: int) -> int:

    res = client.service.FECompUltimoAutorizado(
        Auth=auth,
        PtoVta=pto_v,
        CbteTipo=constants['COD_CMP']
    )

    return int(res['CbteNro'])
