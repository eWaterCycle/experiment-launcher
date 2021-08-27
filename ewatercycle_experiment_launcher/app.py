import os

import connexion
from connexion import RestyResolver
from flask_cors import CORS


def create_app(test_config=None):
    app = connexion.FlaskApp('ewatercycle_experiment_launcher')

    if test_config is None:
        app.app.config['JUPYTERHUB_TOKEN'] = os.environ['JUPYTERHUB_TOKEN']
        app.app.config['JUPYTERHUB_URL'] = os.environ['JUPYTERHUB_URL']
        app.app.config['JWT_SECRET'] = os.environ['JWT_SECRET']
    else:
        app.app.config.update(test_config)

    base_path = os.environ.get('BASE_PATH', '')
    resolver = RestyResolver('ewatercycle_experiment_launcher.api')
    app.add_api('openapi.yaml',
                resolver=resolver,
                validate_responses=True,
                base_path=base_path)
    CORS(app.app)
    return app
