from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings
from app.core.exceptions import InvalidAccessTokenError

ALGORITHM = "HS256"


def create_access_token(subject: str) -> tuple[str, int]:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    claims = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
        "iss": settings.JWT_ISSUER,
    }
    token = jwt.encode(
        claims,
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=ALGORITHM,
    )
    return token, settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60


def get_admin_id_from_access_token(token: str) -> int:
    try:
        claims = jwt.decode(
            token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[ALGORITHM],
            issuer=settings.JWT_ISSUER,
            options={"require": ["exp", "iat", "sub", "iss"]},
        )
        subject = claims["sub"]
        if not isinstance(subject, str) or not subject.isdecimal():
            raise InvalidAccessTokenError
        admin_id = int(subject)
        if admin_id <= 0:
            raise InvalidAccessTokenError
        return admin_id
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError, OverflowError) as exc:
        raise InvalidAccessTokenError from exc