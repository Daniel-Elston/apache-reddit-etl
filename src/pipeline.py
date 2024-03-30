from __future__ import annotations

import json
import logging
import time

from config import my_vars
from src.data.extract import ExtractData
from src.data.hdfs import HFSManagement
from src.data.producer import KafkaSender
from utils.setup_env import setup_project_env

project_dir, config, setup_logs = setup_project_env()
CREDS, KAFKA_BROKER_URL, KAFKA_TOPIC = my_vars()


class Pipeline:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def main(self):
        subreddit_name = 'funny'
        filename = f"{subreddit_name}_{int(time.time())}.json"
        hdfs_filepath = f"data/hdfs/{filename}"

        extract_manager = ExtractData(CREDS)
        produce_manager = KafkaSender(KAFKA_TOPIC, KAFKA_BROKER_URL)
        hdfs_manager = HFSManagement(hdfs_filepath)

        def callback(data):

            # Hadoop
            data_str = json.dumps(data)
            hdfs_manager.save_to_hdfs(data_str.encode('utf-8'))

            # Kafka
            produce_manager.send_to_kafka(data)

        extract_manager.stream_comments(subreddit_name, callback)


# if __name__ == '__main__':
#     Pipeline.main()
