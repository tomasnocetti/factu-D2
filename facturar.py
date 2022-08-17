from copyreg import constructor
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7

import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

from src.service import solicitar_ta

with open('config/certificado.pem', 'rb') as cert_file:
    cert_buf = cert_file.read()

with open('config/clave.key', 'rb') as key_file:
    key_buf = key_file.read()


def generar_solicitud_xml():
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

    return solicitudXML


def generar_solicitud_ta(cms: str) -> str:
    mytree = ET.parse('templates/solicitudLoginCms.xml')
    myroot = mytree.getroot()

    myroot[1][0][0].text = cms

    return ET.tostring(myroot, encoding='unicode')


def xml_a_bytes(xmlcontent):
    return bytes(ET.tostring(xmlcontent.getroot(),
                             encoding='unicode'), 'utf-8')


def generar_cms(certificado: bytes, clave: bytes, contenido: bytes):
    SIGN_HEADER = b'-----BEGIN PKCS7-----\n'
    SIGN_FOOTER = b'-----END PKCS7-----\n'

    cert = x509.load_pem_x509_certificate(certificado)

    key = serialization.load_pem_private_key(clave, None)
    options = []

    cms = pkcs7.PKCS7SignatureBuilder().set_data(
        contenido
    ).add_signer(
        cert, key, hashes.SHA256()
    ).sign(
        serialization.Encoding.PEM, options
    )

    return cms \
        .replace(SIGN_HEADER, b'') \
        .replace(SIGN_FOOTER, b'') \
        .decode("utf-8")


solicitudXML = generar_solicitud_xml()

bufferCMS = xml_a_bytes(solicitudXML)

cms = generar_cms(cert_buf, key_buf, bufferCMS)

solicitudTA = generar_solicitud_ta(cms)

responseXML = solicitar_ta(solicitudTA)

print(ET.tostring(responseXML, encoding='unicode'))
