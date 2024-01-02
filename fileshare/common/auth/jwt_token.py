from datetime import datetime, timedelta
from typing import Annotated
import base64
import jwt as pyjwt
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from fileshare.common.exception import TokenExpiredException, InvalidTokenException


SECRET_KEY = "secretkey" # Put into Environment Variable (Cloud Machine)
ALGORITHM = "HS256"
TOKEN_EXPIRATION_MINUTES = 43800


def create_jwt_token(payload):
    """
    Create a JWT token with the given payload.
    """
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    payload['exp'] = expiration
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def verify_jwt_token(token):
    """
    Verify a JWT token and return the payload if valid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except pyjwt.ExpiredSignatureError:
        raise TokenExpiredException("Token Expired")
    except pyjwt.DecodeError:
        raise InvalidTokenException("Invalid Token")


def decodeJWT(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return decoded_token


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header is missing")
        
        token = self._get_token(authorization)
        payload = self._decode_token(token)
        return payload

    def _get_token(self, authorization: str):
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            return parts[1]
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    def _decode_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")

