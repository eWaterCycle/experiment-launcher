from flask import current_app

from ewatercycle_experiment_launcher.hub import JupyterHubClient


def process_notebook(request, notebook):
    token = current_app.config['JUPYTERHUB_TOKEN']
    jupyterhub_url = current_app.config['JUPYTERHUB_URL']
    username = request['username']
    client = JupyterHubClient(jupyterhub_url, token, username)

    client.start_server()

    directory = request['directory']
    client.create_directory(directory)

    path = directory + '/' + request['filename']
    location = client.upload_notebook(notebook, path)
    return {"location": location}
