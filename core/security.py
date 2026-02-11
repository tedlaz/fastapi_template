from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from core.config import cfg  # SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

ALGORITHM = "HS256"

_password_hash = PasswordHash(
    (
        Argon2Hasher(),
        BcryptHasher(),
    )
)

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(username: str, **kwargs) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=cfg.TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(username)}
    for key, value in kwargs.items():
        to_encode[key] = str(value)
    encoded_jwt = jwt.encode(to_encode, cfg.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any] | None:
    try:
        decoded_token = jwt.decode(token, cfg.SECRET_KEY, algorithms=[ALGORITHM])
        exp = decoded_token.get("exp")

        if exp is None:
            return None

        if isinstance(exp, (int, float)):
            exp_dt = datetime.fromtimestamp(exp, tz=timezone.utc)

        elif isinstance(exp, datetime):
            exp_dt = exp

        else:
            return None

        return decoded_token if exp_dt >= datetime.now(timezone.utc) else None

    except jwt.PyJWTError:
        return None


def verify_hash(plain_text: str, hashed_text: str) -> tuple[bool, str | None]:
    return _password_hash.verify_and_update(plain_text, hashed_text)


def create_hash(text: str) -> str:
    return _password_hash.hash(text)
