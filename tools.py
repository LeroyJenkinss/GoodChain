from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import hashlib
from hashlib import blake2b


def sha256(message):
    return hashlib.sha256(message.encode('UTF-8')).hexdigest()


