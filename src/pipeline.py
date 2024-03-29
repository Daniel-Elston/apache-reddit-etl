from __future__ import annotations

import logging

from config import my_vars
from src.data.extract import ExtractData
from src.data.producer import KafkaSender
from utils.setup_env import setup_project_env

project_dir, config, setup_logs = setup_project_env()
CREDS, KAFKA_BROKER_URL, KAFKA_TOPIC = my_vars()


class Pipeline:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)


def main():
    subreddit_name = 'funny'

    extract_manager = ExtractData(CREDS)
    produce_manager = KafkaSender(KAFKA_TOPIC, KAFKA_BROKER_URL)

    def callback(data):
        produce_manager.send_to_kafka(data)

    extract_manager.stream_comments(subreddit_name, callback)


if __name__ == '__main__':
    main()
