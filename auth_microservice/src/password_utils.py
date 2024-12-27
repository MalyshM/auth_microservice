import os
import hashlib
import binascii

from dotenv import load_dotenv

load_dotenv()
SALT = os.getenv("SALT", "do not use default!")


def hash_password(password: str) -> str:
    iterations = 100000
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), SALT.encode(), iterations
    )
    return binascii.hexlify(dk).decode()


def verify_password(stored_password: str, provided_password: str) -> bool:
    hash_hex = stored_password
    stored_hash = binascii.unhexlify(hash_hex)
    iterations = 100000
    dk = hashlib.pbkdf2_hmac(
        "sha256", provided_password.encode(), SALT.encode(), iterations
    )
    return dk == stored_hash
