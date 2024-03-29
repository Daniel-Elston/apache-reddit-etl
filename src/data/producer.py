from __future__ import annotations

import json
import logging

from kafka import KafkaProducer


class KafkaSender:
    def __init__(self, KAFKA_TOPIC, kafka_broker_url):
        self.kafka_topic = KAFKA_TOPIC
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=kafka_broker_url,
            value_serializer=lambda m: json.dumps(m).encode('ascii'))
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_to_kafka(self, data):
        try:
            self.kafka_producer.send(self.kafka_topic, value=data)
            self.kafka_producer.flush()
        except Exception as e:
            self.logger.error(f"Failed to send data to Kafka: {e}")
