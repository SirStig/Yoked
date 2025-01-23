import jwt
from jwt import PyJWTError
from datetime import datetime
from fastapi import HTTPException
from backend.core.config import settings

def decode_token(token: str) -> dict:
    """
    Decodes and validates a JWT token.

    :param token: The JWT token to decode.
    :return: The decoded payload if the token is valid.
    :raises HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if "exp" in payload and datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")

        return payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")