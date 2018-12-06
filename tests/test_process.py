import re

from ewatercycle_experiment_launcher.api import hello
from ewatercycle_experiment_launcher.hub import JupyterHubClient
from ewatercycle_experiment_launcher.process import process_notebook


class TestProcessNotebook:
    def test_withoutWorkspace(self, mocked_client: JupyterHubClient):
        request = {
            'directory': 'mydir',
            'filename': 'hello.ipynb',
        }
        notebook = hello.notebook()
        location = process_notebook(request, notebook, mocked_client)

        expected = 'https://hub.ewatercycle.org/user/myusername/lab/workspaces/\w{32}/tree/mydir/hello.ipynb'
        assert re.match(expected, location['location'])

    def test_withWorkspace(self, mocked_client: JupyterHubClient):
        request = {
            'directory': 'mydir',
            'filename': 'hello.ipynb',
            'workspace': 'mywp',
        }
        notebook = hello.notebook()
        location = process_notebook(request, notebook, mocked_client)

        expected = 'https://hub.ewatercycle.org/user/myusername/lab/workspaces/mywp/tree/mydir/hello.ipynb'
        assert expected == location['location']
