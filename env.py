import os

env = os.environ.get('ENV') or 'test'

print(f'Running in {env} mode')

constants = {
    'COD_CMP': 11,
    'BASE_QR_URL': 'https://www.afip.gob.ar/fe/qr/?p=',
    'MON_ID': 'PES',
    'MON_COTZ': 1,
    'CUIT_DOC_CODE': 80,
    'CONSUMIDOR_FINAL_DOC_CODE': 99,
    'CONSUMIDOR_FINAL_DOC_N': 0,
    'FACTURACION_SERVICE': 'wsfe',
}

__testing_config = {
    'AUTH_URL': 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms',
    'PRIVATE_KEY': 'config/test/clave.key',
    'CERTIFICATE': 'config/test/certificado.pem',
    'FACTURACION_WSDL': 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL',
    'TMP_AUTH_PATH': 'tmp/auth_test.xml',
    'CUIT': '20396423295'
}

__prod_config = {
    'AUTH_URL': 'https://wsaa.afip.gov.ar/ws/services/LoginCms',
    'PRIVATE_KEY': 'config/prod/clave.key',
    'CERTIFICATE': 'config/prod/certificado.pem',
    'FACTURACION_WSDL': 'https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL',
    'TMP_AUTH_PATH': 'tmp/auth_prod.xml',
    'CUIT': '20396423295'
}

config = __testing_config if env == 'test' else __prod_config

cert_buf = os.environ.get('CERT_BUF')

if (cert_buf != None):
    cert_buf = bytes(cert_buf, 'utf-8')
else:
    with open(config['CERTIFICATE'], 'rb') as cert_file:
        cert_buf = cert_file.read()

key_buf = os.environ.get('KEY_BUF')

if (key_buf != None):
    key_buf = bytes(key_buf, 'utf-8')
else:
    with open(config['PRIVATE_KEY'], 'rb') as key_file:
        key_buf = key_file.read()
