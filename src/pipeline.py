from __future__ import annotations

import logging
import threading

from config import my_vars
from src.data.consumer import listen_to_messages
from src.data.extract import ExtractData
from src.data.producer import KafkaSender
from utils.setup_env import setup_project_env

project_dir, config, setup_logs = setup_project_env()
CREDS, KAFKA_BROKER_URL, KAFKA_TOPIC = my_vars()


class Pipeline:
    """Pipeline class to orchestrate the data pipeline"""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def kafka_stream(self):
        extract_manager = ExtractData(CREDS)
        produce_manager = KafkaSender(KAFKA_TOPIC, KAFKA_BROKER_URL)

        def callback(data):
            """Callback to process data. Data created in the extract stage."""
            produce_manager.send_to_kafka(data)

        # Start the consumer in a separate thread
        consumer_thread = threading.Thread(target=listen_to_messages)
        consumer_thread.start()

        extract_manager.stream_comments(config['subreddit_name'], callback)

    def main(self):
        self.kafka_stream()


if __name__ == '__main__':
    Pipeline().main()
