from unittest.mock import Mock

import pytest

from ewatercycle_experiment_launcher.hub import JupyterHubClient


@pytest.fixture
def mocked_client():
    url = 'https://hub.ewatercycle.org'
    token = 'some-random-string'
    username = 'myusername'
    client = JupyterHubClient(url, token, username)
    # Replace http client by mock
    client.agent = Mock()
    return client
