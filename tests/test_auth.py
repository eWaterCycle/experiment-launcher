from base64 import b64encode

import pytest
from werkzeug.exceptions import Unauthorized

from ewatercycle_experiment_launcher.app import create_app
from ewatercycle_experiment_launcher.auth import check_basic_auth, generate_token, decode_token, JWT_ISSUER


def test_check_basic_auth_wrong():
    assert check_basic_auth('wronguser', 'wrongpassword') is None


@pytest.fixture
def app():
    return create_app({
        'TESTING': True,
        'JUPYTERHUB_TOKEN': 'somejhtoken',
        'JUPYTERHUB_URL': 'https://localhost:8000',
        'JWT_SECRET': 'somejwtsecret'
    })


def test_generate_token(app):
    headers = {
        'Authorization': 'Basic ' + b64encode(b'someuser:somepw').decode('utf-8')
    }
    with app.app.app_context(), app.app.test_request_context('/auth', headers=headers):
        response = generate_token()
        assert len(response['token']) > 100


def test_decode_token_authenicated(app):
    with app.app.app_context():
        headers = {
            'Authorization': 'Basic ' + b64encode(b'someuser:somepw').decode('utf-8')
        }
        with app.app.test_request_context('/auth', headers=headers):
            response = generate_token()
            token = response['token']

        response = decode_token(token)
        assert response['iss'] == JWT_ISSUER
        assert response['sub'] == 'someuser'


def test_decode_token_unauthorized(app):
    with app.app.app_context():
        with pytest.raises(Unauthorized, match=r'Unauthorized'):
            decode_token('somerandometoken')
