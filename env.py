import os

env = os.environ.get('ENV') or 'test'

__testing_config = {
    'AUTH_URL': 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms',
    'PRIVATE_KEY': 'config/test/clave.key',
    'CERTIFICATE': 'config/test/certificado.pem',
    'FACTURACION_WSDL': 'https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL',
    'TMP_AUTH_PATH': 'tmp/auth_test.xml',
    'CUIT': '20396423295'
}

__prod_config = {
    'AUTH_URL': 'https://wsaahomo.afip.gov.ar/ws/services/LoginCms',
    'PRIVATE_KEY': 'config/prod/clave.key',
    'CERTIFICATE': 'config/prod/certificado.pem',
    'FACTURACION_WSDL': 'https://servicios1.afip.gov.ar/wsfev1/service.asmx?WSDL',
    'TMP_AUTH_PATH': 'tmp/auth_prod.xml',
    'CUIT': '20396423295'
}

config = __testing_config if env == 'test' else __prod_config
