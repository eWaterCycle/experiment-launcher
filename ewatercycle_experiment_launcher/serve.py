import logging
import os

import connexion
from connexion import RestyResolver
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp(__name__)
app.app.config['JUPYTERHUB_TOKEN'] = os.environ['JUPYTERHUB_TOKEN']
app.app.config['JUPYTERHUB_URL'] = os.environ['JUPYTERHUB_URL']
resolver = RestyResolver('ewatercycle_experiment_launcher.api')
app.add_api('openapi.yaml', resolver=resolver, validate_responses=True)
CORS(app.app)
