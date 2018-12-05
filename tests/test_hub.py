from io import BytesIO
from unittest.mock import Mock

import pytest
from requests import Response, HTTPError

from ewatercycle_experiment_launcher.hub import JupyterHubClient


def test_construct():
    url = 'https://hub.ewatercycle.org'
    token = 'some-random-string'
    username = 'myusername'
    client = JupyterHubClient(url, token, username)

    assert client.agent and client.agent.headers['Authorization'] == 'token ' + token


@pytest.fixture
def mocked_client():
    url = 'https://hub.ewatercycle.org'
    token = 'some-random-string'
    username = 'myusername'
    client = JupyterHubClient(url, token, username)
    client.agent = Mock()
    return client


class TestStartServer:
    def test_created(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 201
        mocked_client.agent.post.return_value = response

        result = mocked_client.start_server()

        api_url = 'https://hub.ewatercycle.org/hub/api/users/myusername/server'
        mocked_client.agent.post.assert_called_with(api_url)
        hub_url = 'https://hub.ewatercycle.org/user/myusername/'
        assert result == hub_url

    def test_alreadyrunning(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 400
        response.raw = BytesIO(b'{"message": "Server is already running"}')
        mocked_client.agent.post.return_value = response

        result = mocked_client.start_server()

        api_url = 'https://hub.ewatercycle.org/hub/api/users/myusername/server'
        mocked_client.agent.post.assert_called_with(api_url)
        hub_url = 'https://hub.ewatercycle.org/user/myusername/'
        assert result == hub_url

    def test_notok(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 500
        mocked_client.agent.post.return_value = response

        with pytest.raises(HTTPError):
            mocked_client.start_server()


class TestCreateDirectory:
    def test_created(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 201
        mocked_client.agent.put.return_value = response

        mocked_client.create_directory('somedir')

        api_url = 'https://hub.ewatercycle.org/user/myusername/api/contents/somedir'
        request_json = {'type': 'directory'}
        mocked_client.agent.put.assert_called_with(api_url, json=request_json)


class TestUploadNotebook:
    def test_upload_ok(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 201
        mocked_client.agent.put.return_value = response
        notebook = 'notebook contents'
        path = 'notebook.ipynb'
        workspace = 'bar'

        nb_url = mocked_client.upload_notebook(notebook, path, workspace)

        api_url = 'https://hub.ewatercycle.org/user/myusername/api/contents/notebook.ipynb'
        request_json = {'type': 'notebook', 'format': 'json', 'content': 'notebook contents'}
        mocked_client.agent.put.assert_called_with(api_url, json=request_json)
        assert nb_url == 'https://hub.ewatercycle.org/user/myusername/lab/workspaces/bar/tree/notebook.ipynb'
