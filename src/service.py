import requests
import xml.etree.ElementTree as ET
import xml.sax.saxutils as saxutils

LOGIN_CMS_URL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms"


class AlreadyAuthenticated(Exception):
    ERROR = 'coe.alreadyAuthenticated'
    pass


def solicitar_ta(payload: str) -> ET.Element:
    headers = {'content-type': 'text/xml',
               'charset': 'utf-8', 'SOAPAction': 'urn:LoginCms'}

    response = requests.post(LOGIN_CMS_URL, data=payload, headers=headers)

    content = response.content.decode("utf-8")
    unescaped_content = saxutils.unescape(content)
    xml_response = ET.fromstring(unescaped_content)

    if(response.status_code == 500):
        fault_element = xml_response[0][0]
        fault_code = fault_element[0].text
        fault_string = fault_element[1].text

        if(AlreadyAuthenticated.ERROR in fault_code):
            raise AlreadyAuthenticated
        else:
            raise Exception(f'code: {fault_code} \n msg: {fault_string}')

    return xml_response
