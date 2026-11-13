import secrets

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

_password_hasher = PasswordHasher()
_dummy_password_hash = _password_hasher.hash(secrets.token_urlsafe(32))


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(password: str, password_hash: str | None) -> bool:
    encoded_hash = password_hash or _dummy_password_hash
    try:
        return _password_hasher.verify(encoded_hash, password)
    except (InvalidHashError, VerificationError):
        return False


def verify_missing_admin_password(password: str) -> None:
    verify_password(password, _dummy_password_hash)