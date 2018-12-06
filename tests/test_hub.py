from io import BytesIO

import pytest
from requests import Response, ConnectionError

from ewatercycle_experiment_launcher.hub import JupyterHubClient, JupyterHubCommunicationError, JupyterCommunicationError


def test_construct():
    url = 'https://hub.ewatercycle.org'
    token = 'some-random-string'
    username = 'myusername'
    client = JupyterHubClient(url, token, username)

    assert client.agent and client.agent.headers['Authorization'] == 'token ' + token


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

    def test_errorresponse(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 500
        mocked_client.agent.post.return_value = response

        with pytest.raises(JupyterHubCommunicationError):
            mocked_client.start_server()

    def test_offline(self, mocked_client: JupyterHubClient):
        msg = 'Failed to establish a new connection: [Errno 111] Connection refused'
        mocked_client.agent.post.side_effect = ConnectionError(msg)

        with pytest.raises(JupyterHubCommunicationError):
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

    def test_errorresponse(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 500
        mocked_client.agent.put.return_value = response

        with pytest.raises(JupyterCommunicationError):
            mocked_client.create_directory('somedir')

    def test_offline(self, mocked_client: JupyterHubClient):
        msg = 'Failed to establish a new connection: [Errno 111] Connection refused'
        mocked_client.agent.put.side_effect = ConnectionError(msg)

        with pytest.raises(JupyterCommunicationError):
            mocked_client.create_directory('somedir')


class TestUploadNotebook:
    notebook = 'notebook contents'
    path = 'notebook.ipynb'
    workspace = 'bar'

    def test_upload_ok(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 201
        mocked_client.agent.put.return_value = response

        nb_url = mocked_client.upload_notebook(self.notebook, self.path, self.workspace)

        api_url = 'https://hub.ewatercycle.org/user/myusername/api/contents/notebook.ipynb'
        request_json = {'type': 'notebook', 'format': 'json', 'content': 'notebook contents'}
        mocked_client.agent.put.assert_called_with(api_url, json=request_json)
        assert nb_url == 'https://hub.ewatercycle.org/user/myusername/lab/workspaces/bar/tree/notebook.ipynb'

    def test_errorresponse(self, mocked_client: JupyterHubClient):
        response = Response()
        response.status_code = 500
        mocked_client.agent.put.return_value = response

        with pytest.raises(JupyterCommunicationError):
            mocked_client.upload_notebook(self.notebook, self.path, self.workspace)

    def test_offline(self, mocked_client: JupyterHubClient):
        msg = 'Failed to establish a new connection: [Errno 111] Connection refused'
        mocked_client.agent.put.side_effect = ConnectionError(msg)

        with pytest.raises(JupyterCommunicationError):
            mocked_client.upload_notebook(self.notebook, self.path, self.workspace)
