import base64
import hashlib

import bcrypt


def _bcrypt_input(password: str) -> bytes:
    encoded_password: bytes = password.encode('utf-8')
    digest: bytes = hashlib.sha256(encoded_password).digest()
    return base64.b64encode(digest)


def get_password_hash(password: str) -> str:
    """
    Get a password hash with bcrypt (random salt per call).
    """
    pre_hashed_input: bytes = _bcrypt_input(password)
    salt = bcrypt.gensalt()
    hashed: bytes = bcrypt.hashpw(pre_hashed_input, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a bcrypt hash.
    """
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except (ValueError, TypeError):
        return False
