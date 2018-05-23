from decorator import decorator
from simplepam import authenticate
import flask


def check_auth(username, password):
    return authenticate(username, password)


def auth_challenge():
    """Sends a 401 response that enables basic auth"""
    return flask.Response('You have to login with proper credentials', 401,
                          {'WWW-Authenticate': 'Basic realm="Login Required"'})


@decorator
def requires_auth(f: callable, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return auth_challenge()
    return f(*args, **kwargs)
