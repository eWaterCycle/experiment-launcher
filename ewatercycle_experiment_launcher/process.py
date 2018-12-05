from uuid import uuid4

from flask import current_app
import flask

from ewatercycle_experiment_launcher.hub import JupyterHubClient


def build_client() -> JupyterHubClient:
    token = current_app.config['JUPYTERHUB_TOKEN']
    jupyterhub_url = current_app.config['JUPYTERHUB_URL']
    username = flask.request.authorization.username
    return JupyterHubClient(jupyterhub_url, token, username)


def process_notebook(request, notebook):
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
