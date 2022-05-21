from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_public_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import *

import hashlib
from hashlib import blake2b


def sha256(message):
    return hashlib.sha256(str(message).encode('UTF-8')).hexdigest()


def generate_keys():
    privateIn = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = privateIn.private_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    publicIn = privateIn.public_key()
    public_key = publicIn.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return private_key, public_key


def sign(transaction, private):
    private_key = load_pem_private_key(private, password=None)
    signature = private_key.sign(
        bytes(str(transaction), 'UTF-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256())
    return signature


# def verify(message, signature, pbc_ser):
#     # public_key = serialization.load_pem_public_key(pbc_ser)
#     try:
#         output = pbc_ser.verify(
#             signature,
#             bytes(str(message), 'UTF-8'),
#             padding.PSS(
#                 mgf=padding.MGF1(hashes.SHA256()),
#                 salt_length=padding.PSS.MAX_LENGTH
#             ),
#             hashes.SHA256())
#         return True
#     except:
#         return False
def verify(transactionData, sig, public):
    try:
        public_key = load_pem_public_key(public)
        output = public_key.verify(
            sig,
            bytes(str(transactionData), 'UTF-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256())
        return True
    except:
        return False