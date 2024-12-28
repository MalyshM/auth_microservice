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
