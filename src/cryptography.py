from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7


def build_cms(certificado: bytes, clave: bytes, contenido: bytes):
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
