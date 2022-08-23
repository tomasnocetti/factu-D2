# Facturador AFIP

## Documentación

Se realiza basandose en la documentación oficial de los WS de AFIP.
El objetivo es simplificar el proceso de facturación para no tener que emitir facturas a traves del facturador online. Funciona para facturas del tipo C.

## Configuración

Se debe tener los siguientes archivos de configración en la carpeta `config`. Como crearlos se especifica en el tutorial provisto por AFIP.
https://www.afip.gob.ar/ws/WSASS/WSASS_manual.pdf

- certificado.pem : certificado emitido por afip para firmar las solicitudes de autenticación.

- clave.key: clave privada RSA 2048

## Dependencias

- [Cryptography](https://pypi.org/project/cryptography/)
