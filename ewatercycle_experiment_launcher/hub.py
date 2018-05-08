from io import StringIO

import requests
import nbformat


class JupyterHubClient:
    def __init__(self, jupyterhub_url, token, username):
        self.jupyterhub_url = jupyterhub_url
        self.agent = requests.Session()
        self.agent.headers = {'Authorization': 'token %s' % token}
        self.username = username

    def start_server(self):
        url = '{0}/hub/api/users/{1}/server'.format(self.jupyterhub_url, self.username)
        r = self.agent.post(url)
        if r.status_code == 201 or (r.status_code == 400 and 'already running' in r.json()['message']):
            server_url = '{0}/user/{1}/'.format(self.jupyterhub_url, self.username)
            return server_url
        else:
            r.raise_for_status()

    def create_directory(self, path):
        url = '{0}/user/{1}/api/contents/{2}'.format(self.jupyterhub_url, self.username, path)
        content = {'type': 'directory'}
        r = self.agent.put(url, json=content)
        r.raise_for_status()

    def upload_notebook(self, notebook, path):
        url = '{0}/user/{1}/api/contents/{2}'.format(self.jupyterhub_url, self.username, path)
        buffer = StringIO()
        nbformat.write(notebook, buffer, version=4)
        r = self.agent.put(url, data=buffer)
        r.raise_for_status()

