from __future__ import annotations

import json
import logging

from kafka import KafkaProducer


class KafkaSender:
    def __init__(self, KAFKA_TOPIC, KAFKA_BROKER_URL):
        self.kafka_topic = KAFKA_TOPIC
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER_URL,
            max_block_ms=30000,
            value_serializer=lambda m: json.dumps(m).encode('utf-8')
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_to_kafka(self, data):
        try:
            self.kafka_producer.send(
                'reddit_comments', value=data)
            self.kafka_producer.flush()
        except Exception as e:
            self.logger.error(f"Failed to send data to Kafka: {e}")
