import time

from jose import JWTError, jwt
from simplepam import authenticate
from werkzeug.exceptions import Unauthorized
from flask import current_app, request

JWT_ISSUER = 'org.ewatercycle.launcher'
JWT_ALGORITHM = 'HS256'


def check_basic_auth(username, password):
    if authenticate(username, password):
        return {'sub': username}
    return None


def _current_timestamp() -> int:
    return int(time.time())


def generate_token():
    username = request.authorization['username']
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": timestamp,
        "sub": str(username),
    }
    JWT_SECRET = current_app.config['JWT_SECRET']
    return {'token': jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)}


def decode_token(token):
    JWT_SECRET = current_app.config['JWT_SECRET']
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized() from e
