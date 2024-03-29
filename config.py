from __future__ import annotations

import os

from utils.setup_env import setup_project_env
project_dir, config, setup_logs = setup_project_env()


def my_vars():
    CREDS = {
        'client_id': os.getenv('REDDIT_CLIENT_ID'),
        'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
        'user_agent': os.getenv('REDDIT_USER_AGENT'),
        'username': os.getenv('REDDIT_USERNAME'),
        'password': os.getenv('REDDIT_PASSWORD')
    }
    KAFKA_BROKER_URL = os.getenv('KAFKA_BROKER_URL')
    KAFKA_TOPIC = 'reddit_comments'
    return CREDS, KAFKA_BROKER_URL, KAFKA_TOPIC
