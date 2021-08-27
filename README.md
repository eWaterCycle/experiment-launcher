# experiment-launcher

[![Python application](https://github.com/eWaterCycle/experiment-launcher/actions/workflows/python-app.yml/badge.svg)](https://github.com/eWaterCycle/experiment-launcher/actions/workflows/python-app.yml)
[![SonarCloud quality gate](https://sonarcloud.io/api/project_badges/measure?project=experiment-launcher&metric=alert_status)](https://sonarcloud.io/dashboard?id=experiment-launcher)
[![SonarCloud coverage](https://sonarcloud.io/api/project_badges/measure?project=experiment-launcher&metric=coverage)](https://sonarcloud.io/component_measures?id=experiment-launcher&metric=coverage)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1453264.svg)](https://doi.org/10.5281/zenodo.1453264)
[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B%20%20%E2%97%8F%20%20%E2%97%8B-orange)](https://fair-software.eu)

eWaterCycle Experiment Launcher a webservice to generate and launch a Jupyter notebook.

The API of the webservice is described in OpenAPI specification at [openapi.yaml](https://github.com/eWaterCycle/experiment-launcher/blob/master/ewatercycle_experiment_launcher/swagger.yaml) and can be seen in [Swagger UI](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/eWaterCycle/experiment-launcher/master/ewatercycle_experiment_launcher/openapi.yaml)

# Install

Instructions below have been tested on Linux, but should also work on OSX and Windows Subsystem for Linux.

## JupyterHub server

The experiment launcher requires a JupyterHub server.

JupyterHub can be installed with the following commands
```bash
pip3 install jupyterhub jupyterlab
sudo npm install -g configurable-http-proxy
```

JupyterHub must accept calls from the experiment launcher service to start a notebook server for any hub user and upload a notebook.
In the JupyterHub configuration file (jupyterhub_config.py) you must register the experiment launcher as a service with admin permissions and a token which the launcher must use to communicate with JupyterHub.

The token (shared secret) for the launcher can be generated with

```bash
openssl rand -hex 32
```

A JupyterHub config file can be made using the [./jupyterhub_config.py.example](jupyterhub_config.py.example) file with

```bash
cp jupyterhub_config.py.example jupyterhub_config.py
```

Put the generated token in the config file by editing it with your favourite editor

```bash
nano jupyterhub_config.py
```

JupyterHub can be started with

```bash
jupyterhub
```

Test JupyterHub by going to http://localhost:8000 and login with your OS credentials.

## Installation for production

```bash
pip install ewatercycle_experiment_launcher
```

## Installation for development

To install the launcher in development mode clone the repo and run

```bash
pip install -r requirements_dev.txt
```

# Run

The launcher must be given the same token as configured in the JupyterHub config file.

```bash
# Use token from jupyterhub_config.py
export JUPYTERHUB_TOKEN=$(python -c "from traitlets.config import Application;\
    print([s['api_token'] for s in \
    next(Application._load_config_files('jupyterhub_config'))['JupyterHub']['services'] \
    if s['name'] == 'experiment-launcher'][0])")
# JUPYTERHUB_URL is URL where JupyterHub is running. If path like `/jupyter` then origin header is appended.
export JUPYTERHUB_URL=http://172.17.0.1:8000
gunicorn -w 4 -b 0.0.0.0:8888 ewatercycle_experiment_launcher.serve:app
```

Goto http://localhost:8888/ui/ for Swagger UI.

The JupyterHub and Experiment Launcher both use local OS accounts for authentication and authorization.

In the Swagger UI you must authorize before trying an operation.

When running on Internet make sure https is enforced so the authentication is secure.

The webservice by default runs on `/` base path. This can be changed by setting the `BASE_PATH` environment variable.
For example `export BASE_PATH=/launcher` will host the Swagger UI on http://localhost:8888/launcher/ui/ .
