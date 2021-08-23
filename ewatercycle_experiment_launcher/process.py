from typing import Dict
from uuid import uuid4

import connexion
from flask import current_app
from flask import request
from nbformat import NotebookNode

from ewatercycle_experiment_launcher.hub import JupyterHubClient


def build_client() -> JupyterHubClient:
    token = current_app.config['JUPYTERHUB_TOKEN']
    jupyterhub_url = current_app.config['JUPYTERHUB_URL']
    if jupyterhub_url.startswith('/') and request.origin:
        jupyterhub_url = request.origin + jupyterhub_url
    username = connexion.context['user']
    return JupyterHubClient(jupyterhub_url, token, username)


def process_notebook(request: Dict[str, str], notebook: NotebookNode, client: JupyterHubClient=None) -> Dict[str, str]:
    if client is None:
        client = build_client()

    client.start_server()

    directory = request['directory']
    client.create_directory(directory)

    path = directory + '/' + request['filename']

    if 'workspace' in request:
        workspace = request['workspace']
    else:
        workspace = uuid4().hex
    location = client.upload_notebook(notebook, path, workspace)
    return {"location": location}
