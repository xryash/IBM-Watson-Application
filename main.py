import logging

import yaml
import os

from postgres_repository import PostgresConnector
from watson_client import WatsonClient



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

logging.basicConfig(level=logging.INFO)

config_path = os.getenv('CONFIG_PATH', 'application.yaml')
config = load_config(config_path)

events = config['events']
postgres_config = config['postgres']

host, database, port, user, password = prepare_credentials(postgres_config)
repository = PostgresConnector(host, database, port, user, password)

watson = WatsonClient(config, events, repository)
watson.connect()


while True:
    pass
