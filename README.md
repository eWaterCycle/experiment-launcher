# experiment-launcher

[![Build Status](https://travis-ci.org/eWaterCycle/experiment-launcher.svg?branch=master)](https://travis-ci.org/eWaterCycle/experiment-launcher)
[![SonarCloud quality gate](https://sonarcloud.io/api/project_badges/measure?project=experiment-launcher&metric=alert_status)](https://sonarcloud.io/dashboard?id=experiment-launcher)
[![SonarCloud coverage](https://sonarcloud.io/api/project_badges/measure?project=experiment-launcher&metric=coverage)](https://sonarcloud.io/component_measures?id=experiment-launcher&metric=coverage)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1453264.svg)](https://doi.org/10.5281/zenodo.1453264)

eWaterCycle Experiment Launcher a webservice to generate and launch a Jupyter notebook.

The API of the webservice is described in OpenAPI specification at [openapi.yaml](https://github.com/eWaterCycle/experiment-launcher/blob/master/ewatercycle_experiment_launcher/swagger.yaml) and can be seen in [Swagger UI](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/eWaterCycle/experiment-launcher/master/ewatercycle_experiment_launcher/openapi.yaml)

See [CONTRIBUTE]

# Install

## JupyterHub server

The experiment launcher needs to communicate with a Jupyter Hub server.
The JupyterHub server must running with a service which has a known token and has admin rights.

```bash
pip install jupyterhub dockerspawner
sudo npm install -g configurable-http-proxy
cp jupyterhub_config.py.example jupyterhub_config.py
# Generate token
export JUPYTERHUB_TOKEN=$(openssl rand -hex 32)
echo $JUPYTERHUB_TOKEN
# Set token
nano jupyterhub_config.py
docker pull ewatercycle/jupyterlab-experiment-builder
jupyterhub
```

Test JupyterHub by going to http://172.17.0.1:8000 and login with OS credentials.

## Installation for production

```bash
pip install ewatercycle_experiment_launcher
```

## Installation for development

To install the launcher in development mode clone the repo and run

```bash
python setup.py develop
```

# Run

```bash
# JUPYTERHUB_TOKEN env var should be set to same value as token in jupyterhub_config.py
export JUPYTERHUB_URL=http://172.17.0.1:8000
gunicorn -w 4 -b 0.0.0.0:8888 ewatercycle_experiment_launcher.serve:app
```

Goto http://localhost:8888/ui/ for Swagger UI.

The JupyterHub and Experiment Launcher use local OS accounts for authentication and authorization.

In the Swagger UI you must authorize before trying an operation.

When running on Internet make sure https is enforced so the authentication is secure.

