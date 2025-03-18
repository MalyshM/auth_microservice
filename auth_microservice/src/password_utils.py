import base64
import binascii
import hashlib
import os

from dotenv import load_dotenv

load_dotenv()
SALT = os.getenv("SALT", "do not use default!")


def hash_password(password: str) -> str:
    iterations = 100000
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), SALT.encode(), iterations
    )
    return binascii.hexlify(dk).decode()


def generate_code_challenge(code_verifier: str) -> str:
    sha256_hash = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(sha256_hash).decode("utf-8").rstrip("=")
    )
    return code_challenge
