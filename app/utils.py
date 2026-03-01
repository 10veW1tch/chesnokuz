import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from passlib.exc import UnknownHashError
from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def generate_slug(title):
    return title.lower().replace(" ", "-")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    if not hashed_password:
        return False

    try:
        return pwd_context.verify(plain_password, hashed_password)
    except UnknownHashError:
        # Fallback for legacy/plaintext records in DB.
        return hmac.compare_digest(plain_password, hashed_password)


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("ascii"))


def _encode_jwt(claims: dict) -> str:
    if settings.ALGORITHM != "HS256":
        raise HTTPException(status_code=500, detail="Only HS256 is supported")

    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _base64url_encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    payload_b64 = _base64url_encode(
        json.dumps(claims, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    signature_b64 = _base64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{signature_b64}"


def _decode_jwt(token: str) -> dict:
    if settings.ALGORITHM != "HS256":
        raise HTTPException(status_code=500, detail="Only HS256 is supported")

    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token format") from exc

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    provided_signature = _base64url_decode(signature_b64)

    if not hmac.compare_digest(expected_signature, provided_signature):
        raise HTTPException(status_code=401, detail="Invalid token signature")

    try:
        payload = json.loads(_base64url_decode(payload_b64))
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token payload") from exc

    return payload


def generate_jwt_tokens(user_id: int, is_access_only: bool = False):
    access_token = _encode_jwt(
        {
            "sub": str(user_id),
            "exp": int(
                (
                    datetime.now(timezone.utc)
                    + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                ).timestamp()
            ),
        }
    )

    if is_access_only:
        return access_token

    refresh_token = _encode_jwt(
        {
            "sub": str(user_id),
            "exp": int(
                (
                    datetime.now(timezone.utc)
                    + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
                ).timestamp()
            ),
        }
    )

    return access_token, refresh_token


def decode_jwt_token(token: str):
    payload = _decode_jwt(token)
    if "sub" not in payload or "exp" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token claims")
    return payload
