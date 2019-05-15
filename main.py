import logging
import sys

import yaml
import os

from postgres_repository import PostgresConnector
from watson_client import WatsonClient

from PyQt5.QtWidgets import QApplication

from gui.main_form import MainForm


def load_config(config_path):
    """Load YAML configuration"""
    with open(config_path, 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
    return config


def prepare_credentials(postgres_config):
    """Extract postgres params from configuration"""
    host = postgres_config['host']
    database = postgres_config['database']
    port = postgres_config['port']
    user = postgres_config['user']
    password = postgres_config['password']
    return host, database, port, user, password


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    config_path = os.getenv('CONFIG_PATH', 'application.yaml')
    config = load_config(config_path)

    events = config['events']
    postgres_config = config['postgres']

    host, database, port, user, password = prepare_credentials(postgres_config)

    repository = PostgresConnector(host, database, port, user, password)

    watson = WatsonClient(logger, config, events, repository)

    app = QApplication(sys.argv)
    ex = MainForm(logger, watson, repository)
    sys.exit(app.exec_())
