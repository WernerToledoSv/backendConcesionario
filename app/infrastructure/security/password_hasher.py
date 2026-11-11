import hashlib
import base64

from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prepare(plain_password: str) -> str:
    """
    Pre-hashea el password con SHA-256 y lo codifica en base64
    antes de pasarlo a bcrypt, evitando el límite de 72 bytes.
    """
    digest = hashlib.sha256(plain_password.encode("utf-8")).digest()
    return base64.b64encode(digest).decode("utf-8")


class PasswordHasher:
    def hash(self, plain_password: str) -> str:
        return _pwd_context.hash(_prepare(plain_password))

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(_prepare(plain_password), hashed_password)
