import logging

from ewatercycle_experiment_launcher.app import create_app

logging.basicConfig(level=logging.INFO)
app = create_app()
