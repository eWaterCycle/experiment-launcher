# experiment-launcher

eWaterCycle Experiment Launcher a webservice to generate and launch a Jupyter notebook.

# Install

Requirements:
- Python >=3.5
- Docker server
- Node >=8

## JupyterHub server

Startup a JupyterHub server running with a service which has a known token and has admin rights.

```bash
pip install jupyterhub dockerspawner
npm install configurable-http-proxy
cp jupyterhub_config.py.example jupyterhub_config.py
# Generate token
JUPYTERHUB_TOKEN=$(openssl rand -hex 32)
echo $JUPYTERHUB_TOKEN
# Set token 
nano jupyterhub_config.py
jupyterhub
```

Test JupyterHub by going to http://172.17.0.1:8000 and login with OS credentials.

Install the launcher

```bash
python setup.py develop
```

# Run

```bash
# JUPYTERHUB_TOKEN env var should be set to same value as token in jupyterhub_config.py
export JUPYTERHUB_URL=http://172.17.0.1:8000
gunicorn -b 0.0.0.0:8888 ewatercycle_experiment_launcher.serve:app
```

Goto http://localhost:8888/ui/ for Swagger UI
