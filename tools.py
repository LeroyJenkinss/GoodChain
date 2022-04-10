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
    return hashlib.sha256(message.encode('UTF-8')).hexdigest()

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
