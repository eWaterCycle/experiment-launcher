import requests
from connexion import ProblemException
from requests import RequestException


class JupyterHubCommunicationError(ProblemException):
    def __init__(self, cause):
        super().__init__(status=500,
                         title='Failed to communicate with Jupyter Hub api',
                         detail=str(cause))


class JupyterCommunicationError(ProblemException):
    def __init__(self, cause):
        super().__init__(status=500,
                         title='Failed to communicate with Jupyter Notebook server api',
                         detail=str(cause))


class JupyterHubClient:
    def __init__(self, jupyterhub_url, token, username):
        self.jupyterhub_url = jupyterhub_url
        self.agent = requests.Session()
        self.agent.headers = {'Authorization': 'token %s' % token}
        self.username = username

    def start_server(self):
        """Starts Jupyter notebook server for user with `username`.

        When server is already running will also be successful.
        """
        url = '{0}/hub/api/users/{1}/server'.format(self.jupyterhub_url, self.username)
        try:
            r = self.agent.post(url)
            if r.status_code == 201 or (r.status_code == 400 and 'already running' in r.json()['message']):
                server_url = '{0}/user/{1}/'.format(self.jupyterhub_url, self.username)
                return server_url
            else:
                r.raise_for_status()
        except RequestException as e:
            raise JupyterHubCommunicationError(e) from e

    def create_directory(self, path):
        url = '{0}/user/{1}/api/contents/{2}'.format(self.jupyterhub_url, self.username, path)
        content = {'type': 'directory'}
        try:
            r = self.agent.put(url, json=content)
            r.raise_for_status()
        except RequestException as e:
            raise JupyterCommunicationError(e) from e

    def upload_notebook(self, notebook, path, workspace):
        api_url = '{0}/user/{1}/api/contents/{2}'.format(self.jupyterhub_url, self.username, path)
        content = {'type': 'notebook', 'format': 'json', 'content': notebook}
        try:
            r = self.agent.put(api_url, json=content)
            r.raise_for_status()
        except RequestException as e:
            raise JupyterCommunicationError(e) from e
        nb_url = '{0}/user/{1}/lab/workspaces/{3}/tree/{2}'.format(self.jupyterhub_url, self.username, path, workspace)
        return nb_url
